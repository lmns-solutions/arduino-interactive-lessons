#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Safe Markdown translator for Jekyll + Just the Docs + Polyglot.

- Preserves YAML front matter, Liquid tags, code fences, inline code, HTML blocks,
  Kramdown attribute lists ({: .class}), and URLs.
- Translates only human-readable text using Google Cloud Translation v2.
- Translates link/alt text but keeps URLs intact.
- Keeps blockquote (>) markers and list markers (-, *, 1.) intact.

Usage:
  export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/your-gcp-sa.json
  pip install google-cloud-translate
  python scripts/translate_markdown_safely.py \
      --src index.md \
      --dst _i18n/bg/index.md \
      --lang bg
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Google Cloud Translate v2
try:
    from google.cloud import translate_v2 as translate
except Exception:
    translate = None

# --------------------------- Regex patterns ---------------------------------
FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
CODE_FENCE   = re.compile(r"```[^\n]*\n.*?```", re.S)
INLINE_CODE  = re.compile(r"`[^`\n]+`")
LIQUID       = re.compile(r"\{\%.*?\%\}|\{\{.*?\}\}", re.S)
ATTR_LIST    = re.compile(r"\{\:\s*[^}]+\}")
HTML_BLOCK   = re.compile(r"<[^>]+>(?:.*?</[^>]+>)?", re.S)

MD_LINK  = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<url>[^)\s]+)(?:\s+\"(?P<title>[^\"]*)\")?\)")
MD_IMAGE = re.compile(r"\!\[(?P<alt>[^\]]*)\]\((?P<url>[^)\s]+)(?:\s+\"(?P<title>[^\"]*)\")?\)")

LINE_PREFIX = re.compile(r"^(?P<prefix>(?:\s{0,3}[\>\s]*)?(?:\s{0,3}(?:[-*+]|\d+\.)\s+)*)")

# --------------------------- Helpers ----------------------------------------
def split_front_matter(text: str) -> Tuple[str, str]:
    m = FRONT_MATTER.match(text)
    if m:
        return m.group(1), m.group(2)
    return None, text

def _placeholder(idx: int) -> str:
    return f"<<<__TK{idx}__>>>"

def _collect_tokens(text: str) -> Tuple[str, Dict[str, str]]:
    token_map: Dict[str, str] = {}
    patterns = [CODE_FENCE, INLINE_CODE, LIQUID, HTML_BLOCK, ATTR_LIST]
    idx = 0
    for pat in patterns:
        def repl(m):
            nonlocal idx
            ph = _placeholder(idx)
            token_map[ph] = m.group(0)
            idx += 1
            return ph
        text = pat.sub(repl, text)

    def link_repl(m):
        nonlocal idx
        ph = _placeholder(idx)
        token_map[ph] = m.group(0)
        idx += 1
        return ph

    text = MD_LINK.sub(link_repl, text)
    text = MD_IMAGE.sub(link_repl, text)

    return text, token_map

def _rebuild_links(masked: str, token_map: Dict[str, str], translator, target_lang: str) -> str:
    new_map: Dict[str, str] = {}
    texts_to_translate: List[str] = []
    order: List[Tuple[str, str, str, str]] = []

    for ph, original in token_map.items():
        m1 = MD_LINK.fullmatch(original or "")
        m2 = MD_IMAGE.fullmatch(original or "")
        if m1:
            texts_to_translate.append(m1.group("text"))
            order.append(("link", ph, m1.group("url"), m1.group("title")))
        elif m2:
            texts_to_translate.append(m2.group("alt"))
            order.append(("image", ph, m2.group("url"), m2.group("title")))

    if texts_to_translate and translator is not None:
        res = translator.translate(texts_to_translate, target_language=target_lang, format_="text")
        translated_list = [r["translatedText"] for r in res]
    else:
        translated_list = []

    ti = 0
    for kind, ph, url, title in order:
        t = translated_list[ti] if ti < len(translated_list) else ""
        ti += 1
        if kind == "link":
            rebuilt = f"[{t}]({url} \"{title}\")" if title else f"[{t}]({url})"
        else:
            rebuilt = f"![{t}]({url} \"{title}\")" if title else f"![{t}]({url})"
        new_map[ph] = rebuilt

    token_map.update(new_map)

    def put_back(m):
        ph = m.group(0)
        return token_map.get(ph, ph)

    return re.sub(r"<<<__TK\d+__>>>", put_back, masked)

def _translate_text_preserving_prefixes(text: str, translator, target_lang: str) -> str:
    out_lines = []
    for line in text.splitlines():
        if not line.strip():
            out_lines.append(line)
            continue
        m = LINE_PREFIX.match(line)
        prefix = m.group("prefix") if m else ""
        rest = line[len(prefix):]
        if translator is not None and rest.strip():
            res = translator.translate(rest, target_language=target_lang, format_="text")
            tr = res["translatedText"]
        else:
            tr = rest
        out_lines.append(prefix + tr)
    return "\n".join(out_lines)

def translate_markdown(md: str, target_lang: str = "bg") -> str:
    translator = translate.Client() if translate is not None else None
    fm, body = split_front_matter(md)
    masked, token_map = _collect_tokens(body)
    translated_body = _translate_text_preserving_prefixes(masked, translator, target_lang)
    translated = _rebuild_links(translated_body, token_map, translator, target_lang)
    if fm:
        if re.search(r"(?m)^lang\s*:", fm):
            fm = re.sub(r"(?m)^lang\s*:.*$", f"lang: {target_lang}", fm)
        else:
            fm += f"\nlang: {target_lang}"
        return f"---\n{fm}\n---\n{translated}\n"
    else:
        return translated

def translate_file(src: Path, dst: Path, lang: str):
    text = src.read_text(encoding="utf-8")
    out = translate_markdown(text, target_lang=lang)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    print(f"Translated: {src} -> {dst}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=str, help="Single source markdown file")
    ap.add_argument("--dst", type=str, help="Destination markdown file")
    ap.add_argument("--lang", type=str, default="bg", help="Target language code (default: bg)")
    args = ap.parse_args()

    if args.src and args.dst:
        translate_file(Path(args.src), Path(args.dst), args.lang)
    else:
        print("Use --src and --dst to translate one file.")

if __name__ == "__main__":
    main()

