#!/usr/bin/env python3
import re
import sys
import pathlib
from typing import Optional, Dict

REPO = pathlib.Path(".").resolve()
SKIP_DIRS = {"_site", "node_modules", "vendor", ".git"}
LANG_SUFFIXES = {"-bg", "-en"}

INLINE = re.compile(
    r'(?<!\!)\[(?P<text>[^\]]+)\]\('
    r'(?P<url>(?!https?:|#|mailto:|tel:|//|{{)[^)]+?\.md)'
    r'(?P<anchor>#[^)]+)?\)'
)

REFDEF = re.compile(
    r'^(?P<prefix>\[[^\]]+\]:\s*)'
    r'(?P<url>(?!https?:|#|mailto:|tel:|//|{{)\S+?\.md)'
    r'(?P<anchor>#\S+)?\s*$',
    re.M
)

def should_skip(p: pathlib.Path) -> bool:
    return any(seg in SKIP_DIRS for seg in p.parts)

def strip_lang_suffix(stem: str) -> str:
    for suf in LANG_SUFFIXES:
        if stem.endswith(suf):
            return stem[: -len(suf)]
    return stem

def slugify(s: str) -> str:
    s = s.replace(" ", "-")
    return re.sub(r"[^A-Za-z0-9_-]", "", s)

def compute_page_id(relpath: pathlib.Path) -> str:
    parts = list(relpath.parts)
    stem = strip_lang_suffix(relpath.stem)
    parts[-1] = stem
    parts = [p for p in parts if p not in (".", "")]
    joined = "-".join(parts) if parts else stem
    return slugify(joined)

def parse_front_matter_page_id(file_path: pathlib.Path) -> Optional[str]:
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    fm_block = "\n".join(lines[1:end])
    m = re.search(r'^\s*page_id\s*:\s*(.+?)\s*$', fm_block, re.M)
    return m.group(1).strip() if m else None

def build_page_id_map() -> Dict[pathlib.Path, str]:
    mapping: Dict[pathlib.Path, str] = {}
    for p in REPO.rglob("*.md"):
        if should_skip(p):
            continue
        try:
            rel = p.resolve().relative_to(REPO)
        except Exception:
            continue
        pid = parse_front_matter_page_id(p) or compute_page_id(rel)
        mapping[p.resolve()] = pid
    return mapping

def resolve_url(from_file: pathlib.Path, url: str) -> Optional[pathlib.Path]:
    url = url.strip()
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1].strip()
    if url.startswith("/"):
        candidate = (REPO / url.lstrip("/")).resolve()
    else:
        candidate = (from_file.parent / url).resolve()
    try:
        candidate.relative_to(REPO)
    except Exception:
        return None
    return candidate if candidate.exists() else None

def liquid_escape_param(val: str) -> str:
    # Prefer single-quoted attributes; escape single quotes
    # Also neutralize Liquid braces inside text to avoid parser confusion
    val = val.replace("'", "&#39;")
    val = val.replace("{", "&#123;").replace("}", "&#125;")
    val = val.replace("\n", " ").replace("\r", " ")
    return val

def rewrite_text(path: pathlib.Path, text: str, pid_map: Dict[pathlib.Path, str]) -> str:
    def repl_inline(m):
        raw_url = m.group("url")
        anchor = m.group("anchor") or ""
        target = resolve_url(path, raw_url)
        if not target:
            return m.group(0)
        target = target.resolve()
        pid = pid_map.get(target)
        if not pid:
            try:
                rel = target.relative_to(REPO)
                pid = compute_page_id(rel)
            except Exception:
                return m.group(0)
        link_text = liquid_escape_param(m.group("text"))
        pid_esc = liquid_escape_param(pid)
        return f"{{% include tlink.html id='{pid_esc}' text='{link_text}' %}}{anchor}"

    def repl_refdef(m):
        raw_url = m.group("url")
        anchor = m.group("anchor") or ""
        target = resolve_url(path, raw_url)
        if not target:
            return m.group(0)
        target = target.resolve()
        pid = pid_map.get(target)
        if not pid:
            try:
                rel = target.relative_to(REPO)
                pid = compute_page_id(rel)
            except Exception:
                return m.group(0)
        pid_esc = liquid_escape_param(pid)
        return f"{m.group('prefix')}{{% include tlink.html id='{pid_esc}' text='' %}}{anchor}"

    new = INLINE.sub(repl_inline, text)
    new = REFDEF.sub(repl_refdef, new)
    return new

def main() -> int:
    pid_map = build_page_id_map()
    changed = 0
    for md in REPO.rglob("*.md"):
        if should_skip(md):
            continue
        original = md.read_text(encoding="utf-8")
        updated = rewrite_text(md.resolve(), original, pid_map)
        if updated != original:
            md.write_text(updated, encoding="utf-8")
            print(f"updated: {md.relative_to(REPO)}")
            changed += 1
    print(f"\nDone. Files updated: {changed}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
