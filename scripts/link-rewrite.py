#!/usr/bin/env python3
import re, sys, pathlib

REPO = pathlib.Path(".").resolve()

# Inline links: [text](path.md#anchor)
INLINE = re.compile(
    r'(?<!\!)\[(?P<text>[^\]]+)\]\('
    r'(?P<url>(?!https?:|#|mailto:|tel:|//|{{)[^)\s]+?\.md)'
    r'(?P<anchor>#[^)]+)?\)'
)

# Reference-style definitions: [ref]: path.md#anchor
REFDEF = re.compile(
    r'^(?P<prefix>\[[^\]]+\]:\s*)'
    r'(?P<url>(?!https?:|#|mailto:|tel:|//|{{)\S+?\.md)'
    r'(?P<anchor>#\S+)?\s*$',
    re.M
)

SKIP_DIRS = {"_site", "node_modules", "vendor", ".git"}

def resolve_url(from_file: pathlib.Path, url: str) -> pathlib.Path | None:
    """Resolve a markdown link URL (which may include ../) to a repo-absolute file path."""
    # Root-relative (starts with /): strip leading slash and resolve from repo
    if url.startswith("/"):
        target = (REPO / url.lstrip("/")).resolve()
    else:
        target = (from_file.parent / url).resolve()
    # Only return if inside the repo and exists
    try:
        target.relative_to(REPO)
    except ValueError:
        return None
    return target if target.exists() else None

def page_id_from_path(p: pathlib.Path) -> str:
    stem = p.stem  # filename without .md
    if stem.endswith("-bg"):
        stem = stem[:-3]
    # keep only safe chars for page_id
    return re.sub(r'[^A-Za-z0-9_-]', '', stem)

def rewrite_text(path: pathlib.Path, text: str) -> str:
    def repl_inline(m):
        raw_url = m.group("url")
        anchor = m.group("anchor") or ""
        target = resolve_url(path, raw_url)
        if not target:
            return m.group(0)  # leave untouched if we can't resolve
        pid = page_id_from_path(target)
        link_text = m.group("text")
        return f'{{% include tlink.html id="{pid}" text="{link_text}" %}}{anchor}'

    def repl_refdef(m):
        raw_url = m.group("url")
        anchor = m.group("anchor") or ""
        target = resolve_url(path, raw_url)
        if not target:
            return m.group(0)
        pid = page_id_from_path(target)
        return f'{m.group("prefix")}{{% include tlink.html id="{pid}" text="" %}}{anchor}'

    new = INLINE.sub(repl_inline, text)
    new = REFDEF.sub(repl_refdef, new)
    return new

def should_skip(p: pathlib.Path) -> bool:
    return any(seg in SKIP_DIRS for seg in p.parts)

def main():
    changed = 0
    for p in REPO.rglob("*.md"):
        if should_skip(p):
            continue
        original = p.read_text(encoding="utf-8")
        updated = rewrite_text(p, original)
        if updated != original:
            p.write_text(updated, encoding="utf-8")
            print(f"updated: {p.relative_to(REPO)}")
            changed += 1
    print(f"\nDone. Files updated: {changed}")

if __name__ == "__main__":
    sys.exit(main())

