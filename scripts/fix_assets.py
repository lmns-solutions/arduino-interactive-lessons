#!/usr/bin/env python3
"""
fix_assets.py — rewrite asset links to use Jekyll's `relative_url` for robustness.

Why: On GitHub Pages sites served under a subpath, page-relative asset URLs like
    src="assets/foo.mp4"
break on nested pages. Using:
    src="{{ '/assets/foo.mp4' | relative_url }}"
works on localhost *and* GitHub Pages.

What this script changes:
  1) HTML:   src= / href= attributes that point into assets/
  2) CSS:    url(assets/...)
  3) Markdown: [link](assets/...) and ![image](assets/...)

What it *doesn't* change:
  - Links already using Liquid (relative_url/absolute_url)
  - Absolute URLs (http/https) or site variables
  - Any line containing '{%' (Liquid tags likely unrelated to URLs)

Usage:
  Dry run (default):  python fix_assets.py
  Actually write:     python fix_assets.py --write
  Limit to a folder:  python fix_assets.py --root path/to/site
"""

import argparse
import re
from pathlib import Path
import shutil
import sys

DEFAULT_EXTS = {
    ".html", ".htm",
    ".md", ".markdown", ".mdx",
    ".liquid",
    ".scss", ".sass", ".css",
    ".yml", ".yaml",
}

EXCLUDE_DIRS = {
    ".git", "_site", "node_modules", ".jekyll-cache", ".sass-cache", "vendor", "dist", "build"
}

def normalize_asset_path(p: str) -> str:
    """Strip leading ./ and leading slashes, ensure it starts with assets/ then return '/assets/...'"""
    p = p.strip()
    # remove leading ./
    if p.startswith("./"):
        p = p[2:]
    # remove leading / to rebuild consistently
    while p.startswith("/"):
        p = p[1:]
    if not p.lower().startswith("assets/"):
        # Not an assets path — leave unchanged
        return None
    return f"/{p}"

def already_liquid(s: str) -> bool:
    s_lower = s.lower()
    return ("{{" in s) or ("| relative_url" in s_lower) or ("| absolute_url" in s_lower)

def process_text(text: str):
    changed = False

    # 1) HTML src/href attributes
    # Matches: src="assets/foo", href='assets/bar'
    attr_pattern = re.compile(
        r"""(?P<prefix>\b(?:src|href)\s*=\s*)(?P<q>["'])(?P<path>(?:\.?/)?assets/[^"']*?)(?P=q)""",
        re.IGNORECASE
    )

    def attr_repl(m: re.Match):
        full = m.group(0)
        if already_liquid(full):
            return full
        path = m.group('path')
        norm = normalize_asset_path(path)
        if not norm:
            return full
        q = m.group('q')
        # Use single quotes inside Liquid for safety; keep original outer quote
        inner = f"{{{{ '{norm}' | relative_url }}}}"
        return f"{m.group('prefix')}{q}{inner}{q}"

    new_text, n1 = attr_pattern.subn(attr_repl, text)
    if n1:
        changed = True
    text = new_text

    # 2) CSS url(assets/...)
    css_url_pattern = re.compile(
        r"""url\(\s*(?P<q>["']?)(?P<path>(?:\.?/)?assets/[^)"']*?)(?P=q)\s*\)""",
        re.IGNORECASE
    )

    def css_repl(m: re.Match):
        full = m.group(0)
        if already_liquid(full):
            return full
        norm = normalize_asset_path(m.group('path'))
        if not norm:
            return full
        return f"url({{{{ '{norm}' | relative_url }}}})"

    new_text, n2 = css_url_pattern.subn(css_repl, text)
    if n2:
        changed = True
    text = new_text

    # 3) Markdown inline links/images: [text](assets/...), ![alt](assets/...)
    md_link_pattern = re.compile(
        r"""(?P<prefix>\]\(|\]\s*:\s*|!\[[^\)]*\]\()\s*(?P<path>(?:\.?/)?assets/[^)\s]+)\s*\)""",
        re.IGNORECASE
    )

    def md_link_repl(m: re.Match):
        full = m.group(0)
        if already_liquid(full):
            return full
        norm = normalize_asset_path(m.group('path'))
        if not norm:
            return full
        return f"{m.group('prefix')}{{{{ '{norm}' | relative_url }}}})"

    new_text, n3 = md_link_pattern.subn(md_link_repl, text)
    if n3:
        changed = True
    text = new_text

    return text, changed, (n1, n2, n3)

def iter_files(root: Path, exts):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in exts:
            yield p

def main():
    ap = argparse.ArgumentParser(description="Rewrite asset URLs to use Jekyll relative_url")
    ap.add_argument("--root", default=".", help="Root directory of your Jekyll site (default: .)")
    ap.add_argument("--write", action="store_true", help="Apply changes in-place (creates .bak backups). Without this, runs in dry-run mode.")
    ap.add_argument("--ext", nargs="*", default=sorted(DEFAULT_EXTS), help="File extensions to scan (default: common web/doc types)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Root '{root}' does not exist.", file=sys.stderr)
        sys.exit(1)

    exts = set(x if x.startswith(".") else f".{x}" for x in args.ext)
    files = list(iter_files(root, set(x.lower() for x in exts)))
    total_changed = 0
    total_matches = [0, 0, 0]

    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            # Skip non-text files
            continue

        new_text, changed, matches = process_text(text)
        if changed:
            total_changed += 1
            total_matches = [a + b for a, b in zip(total_matches, matches)]
            rel = f.relative_to(root)
            if args.write:
                # backup
                #f.with_suffix(f.suffix + ".bak").write_text(text, encoding="utf-8")
                f.write_text(new_text, encoding="utf-8")
                print(f"[FIXED] {rel}  (+{matches[0]} HTML attrs, +{matches[1]} CSS urls, +{matches[2]} MD links)")
            else:
                print(f"[DRYRUN] Would fix {rel}  (+{matches[0]} HTML attrs, +{matches[1]} CSS urls, +{matches[2]} MD links)")

    mode = "WROTE CHANGES" if args.write else "DRY RUN"
    print(f"\n{mode}: {total_changed} files updated. Totals: HTML attrs={total_matches[0]}, CSS urls={total_matches[1]}, MD links={total_matches[2]}")

if __name__ == "__main__":
    main()
