#!/usr/bin/env python3
"""
build.py — Static site builder replacing Jekyll.

Usage:
    pip install -r requirements.txt
    python build.py

Output: _site/
"""

import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
    import markdown as mdlib
except ImportError:
    print("Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

ROOT = Path(__file__).parent
SITE = ROOT / "_site"

# Directories/files that never become output pages
SKIP_DIRS = {
    ".git", "_site", "_includes", "_layouts",
    ".jekyll-cache", ".sass-cache", "vendor",
}
SKIP_FILES = {
    "README.md", "CLAUDE.md",
    ".gitignore", "build.py", "requirements.txt",
}
COPY_DIRS  = {"css", "img"}
COPY_FILES = {"CNAME", "robots.txt", "favicon.ico"}

MD_EXTENSIONS = [
    "toc",
    "fenced_code",
    "tables",
    "footnotes",
    "attr_list",
    "codehilite",
    "md_in_html",
]
MD_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False, "css_class": "highlight"},
    "toc": {"permalink": False},
}

REDIRECT_HTML = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url={url}">
  <link rel="canonical" href="{url}">
  <title>Redirecting…</title>
</head>
<body>
  <p>Redirecting to <a href="{url}">{url}</a>…</p>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Config & template loading
# ---------------------------------------------------------------------------

def load_includes() -> dict:
    d = ROOT / "_includes"
    if not d.exists():
        return {}
    return {f.name: f.read_text(encoding="utf-8") for f in d.glob("*") if f.is_file()}


def expand_includes(text: str, includes: dict) -> str:
    """Replace {% include name %} tags only — leave {{ content }} intact."""
    def sub(m):
        name = m.group(1).strip()
        return includes.get(name, f"<!-- include '{name}' not found -->")
    return re.sub(r'\{%-?\s*include\s+(\S+?)\s*-?%\}', sub, text)


def process_liquid(text: str, includes: dict, content: str = "") -> str:
    """Replace {% include name %} tags and {{ content }}."""
    text = expand_includes(text, includes)
    text = text.replace("{{ content }}", content)
    return text


def load_layouts(includes: dict) -> dict:
    """Load layout files (HTML/Liquid despite .md extension) and expand includes."""
    d = ROOT / "_layouts"
    if not d.exists():
        return {}
    layouts = {}
    for f in d.glob("*.md"):
        raw = f.read_text(encoding="utf-8")
        _, body = parse_frontmatter(raw)
        # Expand includes now; {{ content }} is substituted per-page later
        layouts[f.stem] = expand_includes(body, includes)
    return layouts


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple:
    """Return (metadata_dict, body_string) from a file with YAML frontmatter."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
                return meta, parts[2].lstrip("\n")
            except yaml.YAMLError:
                pass
    return {}, text


# ---------------------------------------------------------------------------
# Markdown conversion
# ---------------------------------------------------------------------------

def fix_toc_id(html: str) -> str:
    """
    Python-Markdown toc extension wraps the TOC in <div class="toc"><ul>…</ul></div>.
    The existing CSS targets ul#markdown-toc (kramdown's output), so patch the id in.
    """
    html = re.sub(
        r'<div class="toc">\s*<ul>',
        '<ul id="markdown-toc">',
        html,
    )
    # Remove the now-orphaned closing </div> that followed </ul>
    html = re.sub(r'</ul>\s*</div>', '</ul>', html, count=1)
    return html


def convert_markdown(text: str) -> str:
    conv = mdlib.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_EXTENSION_CONFIGS)
    html = conv.convert(text)
    return fix_toc_id(html)


# ---------------------------------------------------------------------------
# Output path resolution
# ---------------------------------------------------------------------------

def output_path(source: Path, meta: dict) -> Path:
    permalink = meta.get("permalink", "")
    if permalink:
        slug = permalink.strip("/")
        if not slug:
            return SITE / "index.html"
        p = Path(slug)
        # Permalink with explicit extension (e.g. /404.html) → use directly
        if p.suffix:
            return SITE / p
        # Permalink is a directory slug → index.html inside it
        return SITE / slug / "index.html"
    rel = source.relative_to(ROOT)
    if source.suffix in (".md", ".markdown"):
        return SITE / rel.with_suffix(".html")
    return SITE / rel


# ---------------------------------------------------------------------------
# Per-file build
# ---------------------------------------------------------------------------

def build_file(source: Path, layouts: dict, includes: dict) -> None:
    text = source.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    layout_name = meta.get("layout", "")

    if source.suffix in (".md", ".markdown"):
        page_html = convert_markdown(body)
    else:
        # .html files may contain Liquid tags; process them
        page_html = process_liquid(body, includes)

    if layout_name and layout_name in layouts:
        html = layouts[layout_name].replace("{{ content }}", page_html)
    else:
        if layout_name:
            print(f"  WARN: layout '{layout_name}' not found ({source.name}) — rendering without layout")
        html = page_html

    dest = output_path(source, meta)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"  {source.relative_to(ROOT)}  →  _site/{dest.relative_to(SITE)}")

    # Also write to filename/index.html so extensionless URLs work
    if dest.name != "index.html" and dest.suffix == ".html":
        dir_dest = dest.with_suffix("") / "index.html"
        dir_dest.parent.mkdir(parents=True, exist_ok=True)
        dir_dest.write_text(html, encoding="utf-8")

    # Generate redirect stubs for redirect_from frontmatter
    redirects = meta.get("redirect_from") or []
    if isinstance(redirects, str):
        redirects = [redirects]
    canonical = "/" + str(dest.relative_to(SITE))
    for redir in redirects:
        redir_dest = SITE / redir.strip("/") / "index.html"
        redir_dest.parent.mkdir(parents=True, exist_ok=True)
        redir_dest.write_text(REDIRECT_HTML.format(url=canonical), encoding="utf-8")
        print(f"  redirect: {redir}  →  {canonical}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Building site…\n")

    includes = load_includes()
    layouts  = load_layouts(includes)

    # Clean and recreate output directory
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    # Copy static asset directories verbatim
    for name in COPY_DIRS:
        src = ROOT / name
        if src.exists():
            shutil.copytree(src, SITE / name)
            print(f"  copied  {name}/")

    # Copy individual static files
    for name in COPY_FILES:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, SITE / name)
            print(f"  copied  {name}")

    print()

    # Walk all source files and build pages
    for source in sorted(ROOT.rglob("*")):
        if not source.is_file():
            continue

        # Skip anything inside a blocked directory
        rel_parts = source.relative_to(ROOT).parts
        if any(p in SKIP_DIRS or p.startswith(".") for p in rel_parts):
            continue

        if source.name.startswith(".") or source.name in SKIP_FILES:
            continue

        if source.suffix in (".md", ".markdown", ".html"):
            build_file(source, layouts, includes)

    print(f"\nDone — output in _site/")


if __name__ == "__main__":
    main()
