#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, re, html
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from google.cloud import translate_v2 as translate
except Exception:
    translate = None

# --------------------------- Patterns ---------------------------
FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)

# Core “protect these verbatim”:
CODE_FENCE   = re.compile(r"```[^\n]*\n.*?```", re.S)
INLINE_CODE  = re.compile(r"`[^`\n]+`")
# Links/images that use Liquid URLs: mask the WHOLE construct
MD_LINK_LIQUID  = re.compile(r"(?<!\!)\[[^\]]+\]\(\s*\{\{.*?\}\}\s*\)", re.S)
MD_IMAGE_LIQUID = re.compile(r"\!\[[^\]]*\]\(\s*\{\{.*?\}\}\s*\)", re.S)
# Then generic Liquid/HTML/attrs
LIQUID       = re.compile(r"\{\%.*?\%\}|\{\{.*?\}\}", re.S)
HTML_BLOCK   = re.compile(r"<[^>]+>(?:.*?</[^>]+>)?", re.S)
ATTR_LIST    = re.compile(r"\{\:\s*[^}]+\}")

# Plain Markdown links/images (no Liquid in URL)
MD_LINK  = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)(?:\s+\"(?P<title>[^\"]*)\")?\)")
MD_IMAGE = re.compile(r"\!\[(?P<alt>[^\]]*)\]\((?P<url>[^)\s]+)(?:\s+\"(?P<title>[^\"]*)\")?\)")

# Keep blockquote/list markers
LINE_PREFIX = re.compile(r"^(?P<prefix>(?:\s{0,3}[\>\s]*)?(?:\s{0,3}(?:[-*+]|\d+\.)\s+)*)")

# Placeholder matcher: raw <<<__TK0__>>> OR &lt;&lt;&lt;__TK0__&gt;&gt;&gt; with optional spaces and 3+ angle-brackets
PLACEHOLDER_ANY = re.compile(
    r"(?:<|&lt;){3,}\s*__\s*TK\s*(\d+)\s*__\s*(?:>|&gt;){3,}",
    re.IGNORECASE
)

ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u200e\u200f"), None)  # ZWSP/ZWNJ/ZWJ/LRM/RLM

# --------------------------- Helpers ---------------------------
def split_front_matter(text: str) -> Tuple[str, str]:
    m = FRONT_MATTER.match(text)
    return (m.group(1), m.group(2)) if m else (None, text)

def _placeholder(i: int) -> str:
    return f"<<<__TK{i}__>>>"

def _collect_tokens(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Replace protected spans with placeholders (stored in token_map).
    Handle big/structured items first.
    """
    token_map: Dict[str, str] = {}
    idx = 0

    def sub_all(pat, s):
        nonlocal idx
        def repl(m):
            nonlocal idx
            ph = _placeholder(idx); idx += 1
            token_map[ph] = m.group(0)
            return ph
        return pat.sub(repl, s)

    # Order: code, inline code, links-with-liquid, images-with-liquid, then generic Liquid/HTML/attrs
    for pat in (CODE_FENCE, INLINE_CODE, MD_LINK_LIQUID, MD_IMAGE_LIQUID, LIQUID, HTML_BLOCK, ATTR_LIST):
        text = sub_all(pat, text)

    # Finally, mask plain links/images (so we can translate visible text/alt later)
    for pat in (MD_LINK, MD_IMAGE):
        text = sub_all(pat, text)

    return text, token_map

def _translate_lines_preserving_prefixes(text: str, tr, lang: str) -> str:
    out = []
    for line in text.splitlines():
        if not line.strip():
            out.append(line); continue
        m = LINE_PREFIX.match(line)
        prefix = m.group("prefix") if m else ""
        rest = line[len(prefix):]
        if tr is not None and rest.strip():
            res = tr.translate(rest, target_language=lang, format_="text")
            translated = res["translatedText"]
        else:
            translated = rest
        out.append(prefix + translated)
    return "\n".join(out)

def _rebuild_links_and_restore_all(text: str, token_map: Dict[str, str], tr, lang: str) -> str:
    """
    1) Rebuild MD link/image placeholders (translate only visible text/alt).
    2) Restore *any* placeholder form (raw/escaped/spaced/extra-brackets).
    3) As a belt-and-suspenders fallback, do direct .replace for any leftovers.
    """
    # Collect link/image placeholders
    to_translate: List[str] = []
    order: List[Tuple[str, str, str, str]] = []  # (kind, ph, url, title/alt)
    for ph, original in token_map.items():
        if not isinstance(original, str):
            continue
        m1 = MD_LINK.fullmatch(original)
        m2 = MD_IMAGE.fullmatch(original)
        if m1:
            to_translate.append(m1.group("text"))
            order.append(("link", ph, m1.group("url"), m1.group("title")))
        elif m2:
            to_translate.append(m2.group("alt"))
            order.append(("image", ph, m2.group("url"), m2.group("title")))

    # Translate the visible bits (if any)
    translated_list = []
    if to_translate and tr is not None:
        res = tr.translate(to_translate, target_language=lang, format_="text")
        translated_list = [r["translatedText"] for r in res]

    # Rebuild those placeholders
    ti = 0
    for kind, ph, url, title in order:
        vis = translated_list[ti] if ti < len(translated_list) else ""
        ti += 1
        rebuilt = f"[{vis}]({url} \"{title}\")" if (kind == "link" and title) else \
                  f"[{vis}]({url})" if kind == "link" else \
                  f"![{vis}]({url} \"{title}\")" if title else \
                  f"![{vis}]({url})"
        token_map[ph] = rebuilt

    # Normalize escapes and strip zero-widths
    text = html.unescape(text).translate(ZERO_WIDTH)

    # Regex restore (handles escaped/spaced/extra >)
    def restore_m(m: re.Match) -> str:
        key = f"<<<__TK{m.group(1)}__>>>"
        return token_map.get(key, key)
    text = PLACEHOLDER_ANY.sub(restore_m, text)

    # Fallback: plain string replace for any exact keys still present
    # (fast path; catches any that survived for unusual reasons)
    for ph, val in token_map.items():
        if ph in text:
            text = text.replace(ph, val)

    return text

def translate_markdown(md: str, lang: str = "bg") -> str:
    tr = translate.Client() if translate is not None else None
    fm, body = split_front_matter(md)
    masked, token_map = _collect_tokens(body)
    translated_body = _translate_lines_preserving_prefixes(masked, tr, lang)
    translated = _rebuild_links_and_restore_all(translated_body, token_map, tr, lang)

    if fm:
        if re.search(r"(?m)^lang\s*:", fm):
            fm = re.sub(r"(?m)^lang\s*:.*$", f"lang: {lang}", fm)
        else:
            fm += f"\nlang: {lang}"
        return f"---\n{fm}\n---\n{translated}\n"
    return translated

def translate_file(src: Path, dst: Path, lang: str):
    out = translate_markdown(src.read_text(encoding="utf-8"), lang)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    print(f"Translated: {src} -> {dst}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=str, help="Source .md")
    ap.add_argument("--dst", type=str, help="Destination .md")
    ap.add_argument("--lang", type=str, default="bg")
    args = ap.parse_args()
    if not (args.src and args.dst):
        print("Use --src and --dst"); return
    translate_file(Path(args.src), Path(args.dst), args.lang)

if __name__ == "__main__":
    main()

