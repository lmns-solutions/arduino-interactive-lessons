#!/usr/bin/env python3
"""
remove_permalinks.py

Recursively scan a Jekyll site folder and remove the `permalink`
key from the YAML front matter of every .md file.

Usage:
  python remove_permalinks.py /path/to/site
  python remove_permalinks.py . --dry-run
  python remove_permalinks.py . --no-backup

Notes:
- Only touches lines inside the *top* front matter block (between --- and --- or ...).
- Removes lines whose key is `permalink` (case-insensitive), e.g.:
    permalink: /foo/
    "permalink": "/bar/"
- If the front matter becomes empty after removal (ignoring comments/blank lines),
  the entire front matter block is removed.
- Creates a .bak backup (original contents) unless --no-backup is passed.
"""

from pathlib import Path
import argparse
import re
import sys

FRONT_START_RE = re.compile(r'^\ufeff?---\s*\r?\n')  # allow BOM; must be at very top
FRONT_END_RE = re.compile(r'^(---|\.\.\.)\s*\r?\n$', re.MULTILINE)

# Match a *line* in YAML front matter whose (possibly quoted) key is 'permalink'
# at the start of the line (allowing leading spaces). E.g.:
#   permalink: /x/
#   "permalink": "/x/"
#   'permalink': /x/
PERMALINK_LINE_RE = re.compile(r'^\s*["\']?permalink["\']?\s*:\s*.*$', re.IGNORECASE)

def find_front_matter_bounds(text: str):
    """Return (start_idx, end_idx) of the front matter content (excluding the delimiter lines),
    or (None, None) if no top-of-file front matter is present."""
    # Must start at file top
    if not FRONT_START_RE.match(text):
        return None, None

    # Find the end delimiter after the first line
    # We look for a line that's exactly '---' or '...' (plus whitespace)
    # Starting the search *after* the first newline
    first_nl = text.find('\n')
    if first_nl == -1:
        return None, None

    match_end = FRONT_END_RE.search(text, pos=first_nl + 1)
    if not match_end:
        return None, None

    # Content starts after the first delimiter line (end of line 1)
    content_start = first_nl + 1
    # Content ends right before the ending delimiter's line start
    content_end = match_end.start()
    # Also return the end of the delimiter line to reconstruct later
    delimiter_end = match_end.end()
    return (content_start, content_end, 0, delimiter_end)

def strip_permalink_lines(front_text: str):
    """Remove any line whose key is 'permalink'. Return (new_text, removed_count)."""
    lines = front_text.splitlines(keepends=True)
    new_lines = []
    removed = 0
    for line in lines:
        if PERMALINK_LINE_RE.match(line):
            removed += 1
            continue
        new_lines.append(line)
    return ("".join(new_lines), removed)

def front_matter_is_effectively_empty(front_text: str):
    """Front matter is 'empty' if it contains only blank lines or comments (# ...)."""
    for raw in front_text.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        # Found some substantive content
        return False
    return True

def process_file(path: Path, dry_run: bool = False, backup: bool = True):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read error: {e}"

    bounds = find_front_matter_bounds(text)
    if bounds == (None, None):
        return False, "no front matter"

    content_start, content_end, delim_start_dummy, delimiter_end = bounds
    front = text[content_start:content_end]

    new_front, removed = strip_permalink_lines(front)
    if removed == 0:
        return False, "permalink not present"

    # If now empty (aside from comments/blank), drop the entire front matter block
    if front_matter_is_effectively_empty(new_front):
        new_text = text[delimiter_end:]  # everything after the end delimiter line
        # Also drop the starting delimiter line at top
        # We already excluded it by starting from delimiter_end
    else:
        # Reconstruct: keep the opening '---\n', then the new front, then the closing delimiter line and rest
        # Opening delimiter is from file start to content_start
        opening = text[:content_start]
        closing_and_rest = text[content_end:]  # includes end delimiter line + remainder
        # Replace just the content between delimiters
        new_text = opening + new_front + closing_and_rest

    if dry_run:
        return True, f"would remove {removed} permalink line(s)"
    else:
        try:
            if backup:
                bak = path.with_suffix(path.suffix + ".bak")
                bak.write_text(text, encoding="utf-8")
            path.write_text(new_text, encoding="utf-8")
            return True, f"removed {removed} permalink line(s)"
        except Exception as e:
            return False, f"write error: {e}"

def iter_markdown_files(root: Path):
    for p in root.rglob("*.md"):
        if p.is_file():
            yield p

def main():
    ap = argparse.ArgumentParser(description="Remove 'permalink' from YAML front matter in Jekyll .md files.")
    ap.add_argument("root", nargs="?", default=".", help="Path to Jekyll site root (default: current dir)")
    ap.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")
    ap.add_argument("--no-backup", action="store_true", help="Do not create .bak backups.")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        sys.exit(1)

    total = 0
    changed = 0
    skipped = 0
    for md in iter_markdown_files(root):
        total += 1
        ok, msg = process_file(md, dry_run=args.dry_run, backup=not args.no_backup)
        if ok:
            changed += 1
            status = "CHANGED" if not args.dry_run else "WOULD CHANGE"
        else:
            skipped += 1
            status = "SKIP"
        rel = md.relative_to(root)
        print(f"[{status}] {rel} -> {msg}")

    print(f"\nDone. Examined {total} file(s): {changed} changed, {skipped} skipped.")
    if not args.dry_run and not args.no_backup:
        print("Backups saved as *.bak alongside originals.")

if __name__ == "__main__":
    main()

