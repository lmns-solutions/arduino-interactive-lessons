#!/usr/bin/env python3
"""
Jekyll Missing Assets Fetcher — Liquid-friendly

Scans your Jekyll repo for asset references in Markdown (*.md) files, checks if
those assets exist under the local ./assets/... tree, and if not, tries to
download them from a remote site using one or more candidate remote prefixes.

Key improvements over the earlier version:
- Markdown patterns now accept Liquid blocks and spaces inside parentheses
  (e.g., ![]({{ '/assets/x.png' | relative_url }})).
- HTML <img>/<video>/<source> "src" now supports both single and double quotes.
- Liquid inside URLs is stripped before path normalization.

Example usage:
  python jekyll-missing-assets-fetcher-liquid.py \
    --root . \
    --local-baseurl /arduino-interactive-lessons \
    --remote-base https://makeabilitylab.github.io \
    --remote-try-prefixes "" /physcomp /physcomp/{section}

Tested with Python 3.9+.
"""

from __future__ import annotations
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Set, Tuple
from urllib.parse import urlparse, unquote

import requests

# --- Patterns -----------------------------------------------------------------
# Capture everything up to the closing ')' so we tolerate spaces/Liquid
MARKDOWN_URL_PATTERNS = [
    re.compile(r"!\[[^\]]*\]\((?P<url>[^)]+)\)", re.IGNORECASE),
    re.compile(r"\[[^\]]*\]\((?P<url>[^)]+)\)", re.IGNORECASE),
]

# Handle src with either ' or " and across img/source/video
HTML_SRC_PATTERNS = [
    re.compile(r"<(?:img|source|video)[^>]*?\ssrc=(['\"])(?P<url>[^'\">]+)\1", re.IGNORECASE),
]

ASSETS_KEYWORD = "assets/"
LOCALHOST_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0"}


@dataclass
class Ref:
    md_file: Path
    url_raw: str
    asset_path: str  # normalized "/assets/..."
    local_path: Path
    section: Optional[str]


def debug(msg: str):
    print(msg, file=sys.stderr)


def extract_urls_from_text(text: str) -> List[str]:
    urls: Set[str] = set()
    for pat in MARKDOWN_URL_PATTERNS:
        for m in pat.finditer(text):
            urls.add(m.group("url").strip())
    for pat in HTML_SRC_PATTERNS:
        for m in pat.finditer(text):
            urls.add(m.group("url").strip())
    return list(urls)


def normalize_asset_path(url: str, local_baseurl: str) -> Optional[str]:
    """Return a normalized "/assets/..." path if the URL references assets, else None.

    Accepts absolute http(s) URLs, site-root absolute ("/..."), relative ("assets/..."),
    and Jekyll Liquid forms like `{{ '/assets/..' | relative_url }}`.
    """
    url = unquote(url).strip()

    # Unwrap common Liquid forms like: {{ '/assets/x.png' | relative_url }}
    if "{{" in url and "}}" in url:
        # Pull the first quoted segment containing assets/
        m = re.search(r"[\"'](?P<inner>[^\"']*assets/[^\"']+)[\"']", url)
        if m:
            url = m.group("inner").strip()

    parsed = urlparse(url)

    path = url
    if parsed.scheme in ("http", "https"):
        path = parsed.path
    elif parsed.scheme in ("data",):
        return None  # ignore data URLs

    # Make site-root style
    if not path.startswith("/"):
        path = "/" + path

    # Remove baseurl if present: e.g., /arduino-interactive-lessons/assets/... -> /assets/...
    base = local_baseurl.strip()
    if base:
        if not base.startswith("/"):
            base = "/" + base
        if path.startswith(base + "/"):
            path = path[len(base):]
        elif path == base:
            path = "/"

    if ASSETS_KEYWORD not in path:
        return None

    # Normalize to start exactly with "/assets/"
    idx = path.find(ASSETS_KEYWORD)
    norm = "/" + path[idx:]
    if not norm.startswith("/assets/"):
        norm = "/" + path[idx:]
    return norm


def guess_section_for_file(md_path: Path, root: Path) -> Optional[str]:
    try:
        rel = md_path.relative_to(root)
    except ValueError:
        rel = md_path
    parts = rel.parts
    if len(parts) >= 2:
        first = parts[0]
        if first.lower() != "assets":
            return first
    return None


def candidate_download_urls(asset_path: str, *,
                            url_from_markdown: str,
                            remote_base: str,
                            prefixes: List[str],
                            section: Optional[str]) -> Iterable[str]:
    parsed = urlparse(url_from_markdown)

    # 1) If the original URL is absolute and NOT localhost, try it first.
    if parsed.scheme in ("http", "https") and parsed.netloc and parsed.netloc.split(":")[0] not in LOCALHOST_HOSTS:
        yield url_from_markdown

    # 2) Try composed remote candidates
    for p in prefixes:
        p_fmt = p
        if "{section}" in p and section:
            p_fmt = p.replace("{section}", section)
        elif "{section}" in p and not section:
            continue
        remote_base_norm = remote_base.rstrip("/")
        p_fmt = ("/" + p_fmt.strip("/")) if p_fmt else ""
        ap = asset_path if asset_path.startswith("/") else "/" + asset_path
        yield f"{remote_base_norm}{p_fmt}{ap}"


def ensure_parent_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def download_to(url: str, dest: Path, session: requests.Session, timeout: int = 20) -> Tuple[bool, Optional[str]]:
    try:
        with session.get(url, stream=True, timeout=timeout) as r:
            if r.status_code == 200:
                ensure_parent_dir(dest)
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True, None
            else:
                return False, f"HTTP {r.status_code}"
    except requests.RequestException as e:
        return False, str(e)


def find_markdown_files(root: Path) -> List[Path]:
    return [p for p in root.rglob("*.md") if p.is_file()]


def main():
    ap = argparse.ArgumentParser(description="Fetch missing Jekyll assets from a remote site.")
    ap.add_argument("--root", default=".", help="Root directory of the Jekyll site (default: .)")
    ap.add_argument("--local-baseurl", default="", help="The Jekyll baseurl used in local links, e.g. /arduino-interactive-lessons")
    ap.add_argument("--remote-base", required=True, help="Remote site origin, e.g. https://makeabilitylab.github.io")
    ap.add_argument("--remote-try-prefixes", nargs="*", default=[""],
                    help="List of path prefixes to try (supports {section}). Example: '' /physcomp /physcomp/{section}")
    ap.add_argument("--dry-run", action="store_true", help="Only report what would be downloaded; do not write files")
    ap.add_argument("--verbose", action="store_true", help="Print extra info")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Root not found: {root}", file=sys.stderr)
        sys.exit(2)

    md_files = find_markdown_files(root)
    if args.verbose:
        debug(f"Found {len(md_files)} markdown files under {root}")

    session = requests.Session()
    missing: List[Ref] = []

    # Scan markdown
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md.read_text(errors="ignore")
        urls = extract_urls_from_text(text)
        if not urls:
            continue
        section = guess_section_for_file(md, root)

        for u in urls:
            asset_path = normalize_asset_path(u, args.local_baseurl)
            if not asset_path:
                continue
            local_path = (root / asset_path.lstrip("/"))
            if not local_path.exists():
                missing.append(Ref(md, u, asset_path, local_path, section))

    # De-duplicate by destination path (keep first occurrence for provenance)
    seen: Set[Path] = set()
    uniq_missing: List[Ref] = []
    for ref in missing:
        if ref.local_path in seen:
            continue
        seen.add(ref.local_path)
        uniq_missing.append(ref)

    if not uniq_missing:
        print("✅ No missing assets referenced in markdown (within ./assets).")
        return

    print(f"🔎 Missing assets: {len(uniq_missing)}")
    for ref in uniq_missing:
        print(f" - {ref.asset_path} (referenced in {ref.md_file})")

    # Download phase
    downloaded = 0
    failed: List[Tuple[Ref, List[Tuple[str, str]]]] = []  # ref, [(url, reason), ...]

    for ref in uniq_missing:
        tried: List[Tuple[str, str]] = []
        if args.dry_run:
            print(f"DRY RUN: Would try to fetch -> {ref.asset_path}")
            continue

        for cand in candidate_download_urls(
            ref.asset_path,
            url_from_markdown=ref.url_raw,
            remote_base=args.remote_base,
            prefixes=args.remote_try_prefixes,
            section=ref.section,
        ):
            ok, err = download_to(cand, ref.local_path, session)
            if ok:
                downloaded += 1
                if args.verbose:
                    debug(f"✔ Downloaded {ref.asset_path} from {cand}")
                break
            else:
                tried.append((cand, err or "unknown error"))
        else:
            failed.append((ref, tried))
            if args.verbose:
                debug(f"✖ Failed to fetch {ref.asset_path}")

    if not args.dry_run:
        print(f"\n⬇️  Downloaded: {downloaded}")
        if failed:
            print(f"⚠️  Failed: {len(failed)} (showing attempts)")
            for ref, attempts in failed:
                print(f" - {ref.asset_path} (from {ref.md_file})")
                for url, reason in attempts[:5]:
                    print(f"    • {url}  -> {reason}")
                if len(attempts) > 5:
                    print(f"    • ... {len(attempts) - 5} more attempts omitted ...")


if __name__ == "__main__":
    main()

