#!/usr/bin/env python3
# fix_relative_assets.py
# Resolve ../ and ./ style asset links relative to each file
# and rewrite them to Jekyll {{ '/path' | relative_url }} so they work under any baseurl.
#
# What it rewrites (when the target exists on disk inside --root):
#   - HTML src= / href=
#   - CSS url(...)
#   - Markdown [link](...) and ![img](...)
#
# It resolves candidates like:
#   ../advancedio/assets/images/foo.png
#   ./assets/img.png
#   images/pic.jpg
# …relative to the file's folder, then converts to '/repo/relative/path' | relative_url.
#
# Skips:
#   - http(s):, mailto:, tel:, data:
#   - anchors (#...)
#   - already-liquid ({{ ... }} or | relative_url / | absolute_url)
#   - anything that doesn't exist on disk inside --root
#
# Usage:
#   Dry run:  python fix_relative_assets.py --root /path/to/repo
#   Write:    python fix_relative_assets.py --root /path/to/repo --write
#
import argparse, re, sys
from pathlib import Path

EXCLUDE_DIRS = {'.git', '_site', 'node_modules', '.jekyll-cache', '.sass-cache', 'vendor', 'dist', 'build'}
DEFAULT_EXTS = {'.md', '.markdown', '.mdx', '.html', '.htm', '.liquid', '.css', '.scss', '.sass'}

# Patterns to find URLs
HTML_ATTR = re.compile(r'(?P<prefix>\b(?:src|href)\s*=\s*)(?P<q>["\'])(?P<url>[^"\']+)(?P=q)', re.IGNORECASE)
CSS_URL   = re.compile(r'url\(\s*(?P<q>["\']?)(?P<url>[^)\s]+)(?P=q)\s*\)', re.IGNORECASE)
# Markdown images and links (inline and reference defs)
MD_LINK  = re.compile(r'(?P<prefix>!?\[[^\]]*\]\(|\]\s*:\s*)(?P<url>[^)\s]+)\)', re.IGNORECASE)

def is_skippable(u: str) -> bool:
    u = u.strip()
    if not u: return True
    low = u.lower()
    if low.startswith(('http://','https://','mailto:','tel:','data:')): return True
    if low.startswith('#'): return True
    if '{{' in u or '| relative_url' in low or '| absolute_url' in low: return True
    return False

def resolve_candidate(file_path: Path, root: Path, url: str):
    """Resolve url relative to file_path's parent; return repo-relative POSIX path like '/dir/file' if real, else None"""
    # Strip quotes and whitespace
    url = url.strip().strip('\'"')
    # Ignore absolute-root paths ('/foo/bar'): keep them as-is (we'll still convert to Liquid)
    if url.startswith('/'):
        abs_path = (root / url.lstrip('/')).resolve()
        try:
            abs_path.relative_to(root)
        except ValueError:
            return None
        if abs_path.exists():
            return '/' + abs_path.relative_to(root).as_posix()
        return None
    # Relative paths with ../, ./, or bare names
    candidate = (file_path.parent / url).resolve()
    try:
        rel = candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if candidate.exists():
        return '/' + rel.as_posix()
    return None

def rewrite_text(text: str, file_path: Path, root: Path):
    changed = False
    counts = {'html':0, 'css':0, 'md':0}

    def replace_html(m):
        s = m.group(0)
        url = m.group('url')
        if is_skippable(url): return s
        new_rel = resolve_candidate(file_path, root, url)
        if not new_rel: return s
        new = f"{m.group('prefix')}{m.group('q')}{{{{ '{new_rel}' | relative_url }}}}{m.group('q')}"
        counts['html'] += 1
        return new

    def replace_css(m):
        s = m.group(0)
        url = m.group('url')
        if is_skippable(url): return s
        new_rel = resolve_candidate(file_path, root, url)
        if not new_rel: return s
        counts['css'] += 1
        return f"url({{{{ '{new_rel}' | relative_url }}}})"

    def replace_md(m):
        s = m.group(0)
        url = m.group('url')
        if is_skippable(url): return s
        new_rel = resolve_candidate(file_path, root, url)
        if not new_rel: return s
        counts['md'] += 1
        return f"{m.group('prefix')}{{{{ '{new_rel}' | relative_url }}}})"

    new_text = HTML_ATTR.sub(replace_html, text)
    new_text = CSS_URL.sub(replace_css, new_text)
    new_text = MD_LINK.sub(replace_md, new_text)
    changed = any(counts.values())
    return new_text, changed, counts

def iter_files(root: Path, exts):
    for p in root.rglob('*'):
        if not p.is_file(): continue
        if any(part in EXCLUDE_DIRS for part in p.parts): continue
        if p.suffix.lower() in exts: yield p

def main():
    ap = argparse.ArgumentParser(description='Resolve ../ assets and rewrite to Jekyll relative_url.')
    ap.add_argument('--root', default='.', help='Repository root (default: .)')
    ap.add_argument('--write', action='store_true', help='Apply changes (otherwise dry run)')
    ap.add_argument('--ext', nargs='*', default=sorted(DEFAULT_EXTS), help='Extensions to scan')
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Root '{root}' does not exist.", file=sys.stderr); sys.exit(1)

    exts = set(x if x.startswith('.') else f'.{x}' for x in args.ext)
    files = list(iter_files(root, set(e.lower() for e in exts)))

    total = {'html':0,'css':0,'md':0}
    changed_files = 0
    for f in files:
        try:
            txt = f.read_text(encoding='utf-8')
        except Exception:
            continue
        new_txt, changed, counts = rewrite_text(txt, f, root)
        if changed:
            changed_files += 1
            total = {k: total[k]+counts[k] for k in total}
            if args.write:
                (f.with_suffix(f.suffix + '.bak')).write_text(txt, encoding='utf-8')
                f.write_text(new_txt, encoding='utf-8')
                print(f"[FIXED] {f.relative_to(root)}  (+HTML:{counts['html']} CSS:{counts['css']} MD:{counts['md']})")
            else:
                print(f"[DRYRUN] Would fix {f.relative_to(root)}  (+HTML:{counts['html']} CSS:{counts['css']} MD:{counts['md']})")

    mode = 'WROTE CHANGES' if args.write else 'DRY RUN'
    print(f"\n{mode}: {changed_files} files updated. Totals => HTML:{total['html']} CSS:{total['css']} MD:{total['md']}")

if __name__ == '__main__':
    main()
