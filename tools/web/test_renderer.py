"""Tests for wiki markdown renderer."""
from pathlib import Path


def test_parse_frontmatter():
    from tools.web.renderer import parse_article

    md = """---
title: "Test Article"
type: person
created: 2026-01-01
related: ["[[Other Article]]"]
sources: [diary_2026_01]
---

## Heading

Some content here.
"""
    meta, html = parse_article(md)
    assert meta["title"] == "Test Article"
    assert meta["type"] == "person"
    assert "sources" in meta


def test_frontmatter_missing():
    from tools.web.renderer import parse_article

    md = "## No Frontmatter\n\nJust plain markdown."
    meta, html = parse_article(md)
    assert meta == {}
    assert "<h2" in html


def test_markdown_renders_html():
    from tools.web.renderer import parse_article

    md = """---
title: "Test"
---

## Heading

A paragraph with **bold** and *italic*.

| Col A | Col B |
|---|---|
| 1 | 2 |
"""
    meta, html = parse_article(md)
    assert "<h2" in html
    assert "<strong>bold</strong>" in html
    assert "<em>italic</em>" in html
    assert "<table>" in html


def test_build_title_map(wiki_root):
    from tools.web.renderer import build_title_map

    title_map = build_title_map(wiki_root)
    assert "Alex Mercer" in title_map
    assert title_map["Alex Mercer"] == "people/alex-mercer"
    assert "Yael Cohen" in title_map
    assert "The Thursday Circle — Historical Doubles" in title_map


def test_wikilink_resolved(wiki_root):
    from tools.web.renderer import parse_article, build_title_map

    title_map = build_title_map(wiki_root)
    md = """---
title: "Test"
---

See [[Alex Mercer]] for more.
"""
    meta, html = parse_article(md, title_map=title_map)
    assert 'href="/wiki/people/alex-mercer"' in html
    assert ">Alex Mercer</a>" in html


def test_wikilink_broken():
    from tools.web.renderer import parse_article

    md = """---
title: "Test"
---

See [[Nonexistent Article]] for more.
"""
    meta, html = parse_article(md, title_map={})
    assert "<strong>Nonexistent Article</strong>" in html
    assert "href" not in html


def test_wikilink_bold_mode(wiki_root):
    from tools.web.renderer import parse_article, build_title_map

    title_map = build_title_map(wiki_root)
    md = """---
title: "Test"
---

See [[Alex Mercer]] for more.
"""
    meta, html = parse_article(md, title_map=title_map, wikilinks_as_bold=True)
    assert "<strong>Alex Mercer</strong>" in html
    assert "href" not in html


def test_hebrew_rtl_wrapping():
    from tools.web.renderer import parse_article

    md = """---
title: "Test"
---

The word שלום means peace.
"""
    meta, html = parse_article(md, title_map={})
    assert '<bdi dir="rtl">' in html
    assert "שלום" in html


def test_hebrew_rtl_not_in_frontmatter():
    from tools.web.renderer import parse_article

    md = """---
title: "שלום Group"
---

English content only.
"""
    meta, html = parse_article(md, title_map={})
    assert meta["title"] == "שלום Group"


def test_mixed_hebrew_english():
    from tools.web.renderer import parse_article

    md = """---
title: "Test"
---

Alex said שלום to everyone.
"""
    meta, html = parse_article(md, title_map={})
    assert '<bdi dir="rtl">' in html
    assert "Alex" in html
