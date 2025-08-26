import os, re
from pathlib import Path
from google.cloud import translate_v2 as translate

# ---- CONFIG ----
SRC_DIRS = [
    ".",
    "advancedio",
    "arduino",
    "communication",
    "cpx",
    "electronics",
    "esp32",
    "microcontrollers",
    "sensors",
    "signals",
    "tools"
]  # put your content roots here; "." is repo root

# skip translation for these resources
BLACKLIST = [
    "LICENSE.md",
    "README.md",
    "teaching-notes.md",
    "website-content-ideas.md",
    "website-dev.md",
    "website-install.md"
]

WHITELIST = [
    "accel.md"
]

SRC_GLOBS = ["**/*.md", "**/*.markdown"]
OUT_ROOT = Path("../_i18n/bg")
# ----------------

translate_client = translate.Client()

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
PROTECT = re.compile(r"(```.*?```|`[^`]+`|{%.*?%}|{{.*?}})", re.S)

def split_front_matter(text):
    m = FRONT_MATTER.match(text)
    return (m.group(1), m.group(2)) if m else (None, text)

def translate_chunk(text):
    if not text.strip():
        return text
    res = translate_client.translate(text, target_language="bg")
    return res["translatedText"]

def translate_body(body):
    out, last = [], 0
    for m in PROTECT.finditer(body):
        pre = body[last:m.start()]
        if pre:
            out.append(translate_chunk(pre))
        out.append(m.group(0))  # keep code/Liquid exactly
        last = m.end()
    tail = body[last:]
    if tail:
        out.append(translate_chunk(tail))
    return "".join(out)

def process(src_path, repo_root):
    text = src_path.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)
    t_body = translate_body(body)
    # Preserve front matter; add/override lang
    if fm:
        if re.search(r"(?m)^lang:", fm):
            fm = re.sub(r"(?m)^lang:.*$", "lang: bg", fm)
        else:
            fm += "\nlang: bg"
        out = f"---\n{fm}\n---\n{t_body}"
    else:
        out = t_body

    rel = src_path.relative_to(repo_root)
    out_path = OUT_ROOT / rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    print("Translated:", rel)

def main():
    repo_root = Path("../").resolve()
    seen = set()
    for d in SRC_DIRS:
        root = (repo_root / d).resolve()

        if not root.exists(): continue

        for pattern in SRC_GLOBS:
            for p in root.glob(pattern):
                if len(WHITELIST) > 0 and p.name not in WHITELIST:
                    print("whitelist presented, but file {} not in it, skipping!".format(p.name))
                    continue

                if p.name in BLACKLIST:
                    print("{} is blacklisted for translation, continue with next one".format(p.name))
                    continue

                print("translating {}...".format(p.name))
                if p.is_file() and p.suffix.lower() in [".md", ".markdown"]:
                    # Skip already translated files & files under _site, _i18n/bg
                    if str(p).startswith(str((repo_root / "_site").resolve())): continue
                    if str(p).startswith(str((repo_root / "_i18n/bg").resolve())): continue
                    # Track by absolute path to avoid duplicates from multiple SRC_DIRS
                    ap = p.resolve()
                    if ap not in seen:
                        seen.add(ap)
                        process(ap, repo_root)

if __name__ == "__main__":
    main()

