import argparse, re, html, fnmatch, os, sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from google.cloud import translate_v2 as translate
except Exception:
    translate = None

PLACEHOLDER = "<<<__HTK{}__>>>"
CODE_PAT   = re.compile(r"(?is)<(code|pre)\b[^>]*>.*?</\1>")
SCRIPT_PAT = re.compile(r"(?is)<script\b[^>]*>.*?</script>")
STYLE_PAT  = re.compile(r"(?is)<style\b[^>]*>.*?</style>")

ATTRS = ["alt", "title", "aria-label", "placeholder"]

def mask_blocks(html_text: str):
    token_map = {}
    i = 0
    for pat in (SCRIPT_PAT, STYLE_PAT, CODE_PAT):
        def repl(m):
            nonlocal i
            ph = PLACEHOLDER.format(i); i += 1
            token_map[ph] = m.group(0)
            return ph
        html_text = pat.sub(repl, html_text)
    return html_text, token_map

def unmask_blocks(html_text: str, token_map: Dict[str, str]) -> str:
    html_text = html.unescape(html_text)
    ph_any = re.compile(r"(?:<|&lt;){3,}\s*__\s*HTK\s*(\d+)\s*__\s*(?:>|&gt;){3,}", re.I)
    def restore(m):
        key = PLACEHOLDER.format(int(m.group(1)))
        return token_map.get(key, key)
    html_text = ph_any.sub(restore, html_text)
    # fallback exact restore
    for k, v in token_map.items():
        if k in html_text:
            html_text = html_text.replace(k, v)
    return html_text

def translate_attrs(html_text: str, tr) -> str:
    for attr in ATTRS:
        pat = re.compile(rf'({attr})="([^"]+)"', re.I)
        def repl(m):
            name, val = m.group(1), m.group(2)
            # Skip obvious URLs
            if re.match(r"^\w+://", val):
                return m.group(0)
            if tr is None or not val.strip():
                return m.group(0)
            t = tr.translate(val, target_language="bg", format_="text")["translatedText"]
            return f'{name}="{t}"'
        html_text = pat.sub(repl, html_text)
    return html_text

def set_lang_bg(html_text: str) -> str:
    if re.search(r'<html\b[^>]*\blang=', html_text, flags=re.I):
        html_text = re.sub(r'(<html\b[^>]*\blang=")[^"]*(")', r'\1bg\2', html_text, flags=re.I)
    else:
        html_text = re.sub(r'<html\b', '<html lang="bg"', html_text, count=1, flags=re.I)
    return html_text

def matches_any(path: Path, patterns: List[str]) -> bool:
    if not patterns:
        return False
    s = str(path).replace("\\", "/")
    for pat in patterns:
        if fnmatch.fnmatch(s, pat):
            return True
    return False

def should_process(rel_path: Path, whitelist: List[str], blacklist: List[str]) -> bool:
    # Normalize to posix-like string
    rel = str(rel_path).replace("\\", "/")
    # We only ever process paths under bg/
    if not rel.startswith("bg/") and rel != "bg/index.html":
        return False
    # If whitelist provided, must match one of the patterns
    if whitelist and not matches_any(rel_path, whitelist):
        return False
    # If blacklist provided and matches, skip
    if blacklist and matches_any(rel_path, blacklist):
        return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default="_site")
    ap.add_argument("--whitelist", default="", help="Comma-separated glob patterns relative to site dir, e.g. 'bg/index.html,bg/arduino/**/*.html'")
    ap.add_argument("--blacklist", default="", help="Comma-separated glob patterns relative to site dir")
    ap.add_argument("--translate-attrs", action="store_true", help="Also translate alt/title/aria-label/placeholder attributes")
    ap.add_argument("--dry-run", action="store_true", help="List files but do not modify them")
    args = ap.parse_args()

    if translate is None:
        print("google-cloud-translate is not installed. `pip install google-cloud-translate`", file=sys.stderr)
        sys.exit(1)

    tr = translate.Client()

    site = Path(args.site_dir).resolve()
    bg_root = site / "bg"
    if not bg_root.exists():
        print(f"No {bg_root} found. Build the site first.", file=sys.stderr)
        sys.exit(1)

    whitelist = [p.strip() for p in args.whitelist.split(",") if p.strip()]
    blacklist = [p.strip() for p in args.blacklist.split(",") if p.strip()]

    all_html = sorted([p for p in bg_root.rglob("*.html")])
    to_process = []
    for p in all_html:
        rel = p.relative_to(site)
        if should_process(rel, whitelist, blacklist):
            to_process.append(p)

    if args.dry_run:
        for p in to_process:
            print(f"[DRY RUN] would translate: {p.relative_to(site)}")
        print(f"[DRY RUN] {len(to_process)} file(s) selected")
        return

    for path in to_process:
        rel = path.relative_to(site)
        text = path.read_text(encoding="utf-8")

        masked, tokens = mask_blocks(text)
        translated = tr.translate(masked, target_language="bg", format_="html")["translatedText"]
        if args.translate_attrs:
            translated = translate_attrs(translated, tr)
        translated = unmask_blocks(translated, tokens)
        translated = set_lang_bg(translated)

        path.write_text(translated, encoding="utf-8")
        print(f"Translated: {rel}")

if __name__ == "__main__":
    main()
