#!/usr/bin/env python3
import re
import sys
import pathlib

REPO = pathlib.Path(".").resolve()
SKIP_DIRS = {"_site", "node_modules", "vendor", ".git"}

LANG_SUFFIXES = {"-bg", "-en"}  # extend if you add more: -es, -de, etc.

FRONT_MATTER_OPEN = re.compile(r"^---\s*$", re.M)

def should_skip(p: pathlib.Path) -> bool:
    return any(seg in SKIP_DIRS for seg in p.parts)

def strip_lang_suffix(stem: str) -> str:
    for suf in LANG_SUFFIXES:
        if stem.endswith(suf):
            return stem[: -len(suf)]
    return stem

def slugify(s: str) -> str:
    # keep alnum, dash, underscore; replace spaces with dash
    s = s.replace(" ", "-")
    return re.sub(r"[^A-Za-z0-9_-]", "", s)

def compute_page_id(relpath: pathlib.Path) -> str:
    parts = list(relpath.parts)
    # remove extension and language suffix
    stem = strip_lang_suffix(relpath.stem)
    parts[-1] = stem
    # remove leading '.' or empty segments just in case
    parts = [p for p in parts if p not in (".", "")]
    # join with '-'
    joined = "-".join(parts[:-1] + [parts[-1]]) if parts else stem
    return slugify(joined)

def compute_permalink(relpath: pathlib.Path) -> str:
    # Build POSIX-like URL parts ending with .html
    parts = list(relpath.parts)
    fname = parts[-1]
    stem = strip_lang_suffix(pathlib.Path(fname).stem)
    dir_parts = parts[:-1]

    if fname.lower() == "index.md":
        # root index -> /index.html
        # folder index -> /<folder>/index.html
        if not dir_parts:
            return "/index.html"
        return "/" + "/".join(dir_parts + ["index.html"])
    else:
        # regular file -> /<dir>/<stem>.html  (or /<stem>.html at root)
        if dir_parts:
            return "/" + "/".join(dir_parts + [f"{stem}.html"])
        else:
            return f"/{stem}.html"

def split_front_matter(text: str):
    """
    Returns (front_matter_text_or_None, body_text, has_front_matter: bool).
    Only considers a YAML fm block at the very start of the file.
    """
    if not text.startswith("---"):
        return (None, text, False)

    # find the closing '---' after the first line
    lines = text.splitlines(keepends=True)
    if len(lines) < 2:
        return (None, text, False)

    # find next '---' line after the first
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_text = "".join(lines[: i + 1])  # includes both --- lines
            body_text = "".join(lines[i + 1 :])
            return (fm_text, body_text, True)

    # no closing ---
    return (None, text, False)

def ensure_kv_in_front_matter(fm_text: str, key: str, value: str) -> str:
    """
    Insert or replace a simple 'key: value' at the top-level of fm_text.
    fm_text is assumed to start with '---' and end with '---' on its last line.
    """
    # separate header/footer lines
    lines = fm_text.splitlines()
    if len(lines) < 2:
        # malformed, rebuild fresh
        return f"---\n{key}: {value}\n---\n"

    header = lines[0].strip()  # '---'
    footer_idx = len(lines) - 1
    # find the last '---' (closing marker)
    for i in range(len(lines) - 1, 0, -1):
        if lines[i].strip() == "---":
            footer_idx = i
            break

    content_lines = lines[1:footer_idx]

    # Look for existing key
    key_re = re.compile(rf"^\s*{re.escape(key)}\s*:\s*.*$", re.M)
    content = "\n".join(content_lines)
    if key_re.search(content):
        content = key_re.sub(f"{key}: {value}", content)
    else:
        # insert at the top of content
        content = f"{key}: {value}\n" + content if content.strip() else f"{key}: {value}\n"

    # reconstruct fm
    new_fm = header + "\n" + content.rstrip() + "\n" + lines[footer_idx].strip() + "\n"
    return new_fm

def build_new_front_matter(page_id: str, permalink: str) -> str:
    return f"---\npage_id: {page_id}\npermalink: {permalink}\n---\n"

def process_file(md_path: pathlib.Path) -> bool:
    rel = md_path.resolve().relative_to(REPO)
    if should_skip(rel):
        return False

    content = md_path.read_text(encoding="utf-8")

    page_id = compute_page_id(rel)
    permalink = compute_permalink(rel)

    fm_text, body, has_fm = split_front_matter(content)

    if has_fm and fm_text:
        # Update or insert both keys
        fm_text = ensure_kv_in_front_matter(fm_text, "page_id", page_id)
        fm_text = ensure_kv_in_front_matter(fm_text, "permalink", permalink)
        new_text = fm_text + body
    else:
        # Create new front matter
        fm_text = build_new_front_matter(page_id, permalink)
        new_text = fm_text + content

    if new_text != content:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"updated: {rel.as_posix()}")
        return True
    return False

def main():
    updated = 0
    for md in REPO.rglob("*.md"):
        if should_skip(md):
            continue
        updated |= process_file(md)
    print("\nDone.")

if __name__ == "__main__":
    sys.exit(main())
