---
layout: article
---
<div class="tags" markdown="1">

**Migrating Away from Jekyll** <br> [software](/articles/tags/software), [AI](/articles/tags/ai)

</div>


[TOC]

<a class="prev" href="/articles/2025/TheProgram"> < </a>
<a class="next" href="/articles/2026/scissors-or-lathe"> > </a>

## Background

This site was originally built with [Jekyll](https://jekyllrb.com/), a Ruby-based static site generator. It worked fine for a while, but over time the friction of maintaining a Ruby environment just to build a small personal site started to feel like overkill. 

The new build system is a single Python script — `build.py` — with three dependencies:

- `pyyaml` — frontmatter parsing
- `markdown` — Markdown to HTML conversion
- `pygments` — syntax highlighting

Running `python3 build.py` produces the same `_site/` output that Jekyll used to generate. No Ruby, no Gemfile, no gem version headaches.

The script replicates the subset of Jekyll actually used by this site:

- **Layouts and includes** — the existing Liquid `{% include %}` tags and `{{ content }}` placeholders are handled with a small regex-based processor. No full Liquid implementation needed.
- **Markdown conversion** — Python-Markdown with the `toc`, `fenced_code`, `tables`, `footnotes`, `codehilite`, and `md_in_html` extensions covers everything the articles use.
- **Redirects** — `redirect_from` frontmatter generates meta-refresh stub pages, replicating the `jekyll-redirect-from` plugin.
