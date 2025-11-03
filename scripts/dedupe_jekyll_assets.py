#!/usr/bin/env python3
"""
dedupe_jekyll_assets.py

Deduplicate assets between:
  - <root>/assets/**        (the *root* assets directory)
  - <root>/<section>/assets/**  (any first-level section assets directory)

Rules:
- If a file under root/assets has the same content as a file under any <section>/assets,
  the root/assets file is considered duplicate and will be removed (when --apply is used).
- Matching is by SHA-256 content hash (robust even if filenames differ).
- Default is a dry run (no deletions). Use --apply to actually delete.
- You can export a JSON report with --export path.json.

Usage examples:
  Dry run (default):
    python dedupe_jekyll_assets.py --root .

  Actually delete duplicates from root/assets:
    python dedupe_jekyll_assets.py --root . --apply

  Export a report while deleting:
    python dedupe_jekyll_assets.py --root . --apply --export dedupe_report.json
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

CHUNK_SIZE = 1024 * 1024  # 1 MiB


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: Path) -> List[Path]:
    return [p for p in root.rglob("*") if p.is_file()]


def find_section_asset_dirs(root: Path) -> List[Path]:
    """Find <root>/<section>/assets directories (one level down)."""
    dirs = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if child.name == "assets":
            continue
        assets_dir = child / "assets"
        if assets_dir.is_dir():
            dirs.append(assets_dir)
    return dirs


def build_hash_index(paths: List[Path]) -> Dict[str, List[str]]:
    """Return {sha256: [absolute_path_str, ...]}"""
    index: Dict[str, List[str]] = {}
    for p in paths:
        try:
            # Skip symlinks to be safe
            if p.is_symlink():
                continue
            digest = sha256_file(p)
        except Exception as e:
            print(f"[warn] Skipping unreadable file: {p} ({e})")
            continue
        index.setdefault(digest, []).append(str(p))
    return index


def main():
    ap = argparse.ArgumentParser(description="Deduplicate assets in a Jekyll project.")
    ap.add_argument("--root", type=str, default=".", help="Root directory of the Jekyll project (default: .)")
    ap.add_argument("--apply", action="store_true", help="Apply deletions (otherwise dry-run)")
    ap.add_argument("--export", type=str, default=None, help="Write a JSON report of actions to this path")
    ap.add_argument("--extensions", type=str, default=None,
                    help="Comma-separated list of file extensions to consider (e.g. 'png,jpg,mp4'). "
                         "By default, all files are considered.")
    args = ap.parse_args()

    project_root = Path(args.root).resolve()
    root_assets = project_root / "assets"
    if not root_assets.is_dir():
        print(f"[error] Root assets directory not found: {root_assets}")
        exit(1)

    # Collect section assets dirs
    section_assets_dirs = find_section_asset_dirs(project_root)
    if not section_assets_dirs:
        print("[info] No <section>/assets directories found. Nothing to compare.")
        exit(0)

    # Optional extension filtering
    exts = None
    if args.extensions:
        exts = {"." + e.strip().lower().lstrip(".") for e in args.extensions.split(",") if e.strip()}

    def filter_by_ext(paths: List[Path]) -> List[Path]:
        if not exts:
            return paths
        return [p for p in paths if p.suffix.lower() in exts]

    # Build hash index for section assets (the "keepers")
    section_files: List[Path] = []
    for ad in section_assets_dirs:
        section_files.extend(iter_files(ad))
    section_files = filter_by_ext(section_files)

    print(f"[info] Indexing {len(section_files)} files under section assets...")
    section_index = build_hash_index(section_files)

    # List files in root assets (the "candidates" for deletion if duplicate content exists)
    root_files = filter_by_ext(iter_files(root_assets))
    print(f"[info] Scanning {len(root_files)} files under root assets...")

    duplicates: List[Tuple[str, List[str]]] = []  # (root_file, matching_section_files)
    kept_count = 0

    for rf in root_files:
        if rf.is_symlink():
            continue
        try:
            digest = sha256_file(rf)
        except Exception as e:
            print(f"[warn] Skipping unreadable file: {rf} ({e})")
            continue

        matches = section_index.get(digest)
        if matches:
            duplicates.append((str(rf), matches))
        else:
            kept_count += 1

    # Reporting
    print("\n=== DEDUPLICATION REPORT ===")
    print(f"Root assets files total:  {len(root_files)}")
    print(f"Duplicates to remove:     {len(duplicates)}")
    print(f"Kept (unique) files:      {kept_count}")
    print(f"Mode:                     {'APPLY (will delete)' if args.apply else 'DRY-RUN (no deletion)'}\n")

    for i, (root_file, matches) in enumerate(duplicates, 1):
        print(f"[{i}] DUPLICATE in root: {root_file}")
        # Show up to first 3 matches for brevity
        for m in matches[:3]:
            print(f"    ↳ matches section: {m}")
        if len(matches) > 3:
            print(f"    ...and {len(matches) - 3} more matches")

    # Export report if requested
    if args.export:
        report = {
            "root": str(project_root),
            "root_assets": str(root_assets),
            "mode": "apply" if args.apply else "dry-run",
            "total_root_assets_files": len(root_files),
            "duplicates_to_remove_count": len(duplicates),
            "kept_unique_count": kept_count,
            "duplicates": [{"root_file": rf, "matching_section_files": ms} for rf, ms in duplicates],
        }
        try:
            out_path = Path(args.export).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            print(f"\n[info] Report exported to: {out_path}")
        except Exception as e:
            print(f"[error] Failed to export report to {args.export}: {e}")

    # Apply deletions if requested
    if args.apply and duplicates:
        print("\n=== APPLYING DELETIONS FROM ROOT ASSETS ===")
        deleted = 0
        for root_file, _ in duplicates:
            p = Path(root_file)
            try:
                if p.exists() and p.is_file():
                    os.remove(p)
                    deleted += 1
                    print(f"[del] {root_file}")
            except Exception as e:
                print(f"[error] Failed to delete {root_file}: {e}")
        print(f"\n[done] Deleted {deleted} duplicate file(s) from {root_assets}")
    elif not args.apply:
        print("\n[dry-run] No files were deleted. Use --apply to remove duplicates from root/assets.")


if __name__ == "__main__":
    main()

