"""Wiki markdown renderer with wikilink and RTL support."""
import re
from pathlib import Path

import frontmatter
import markdown


def build_title_map(wiki_root: Path) -> dict[str, str]:
    """Scan wiki directory, return {article_title: relative_url_path} mapping."""
    title_map = {}
    for md_file in wiki_root.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        try:
            post = frontmatter.load(str(md_file))
            title = post.metadata.get("title")
            if title:
                rel = md_file.relative_to(wiki_root).with_suffix("")
                title_map[title] = str(rel).replace("\\", "/")
        except Exception:
            continue
    return title_map


def _replace_wikilinks(text: str, title_map: dict[str, str], as_bold: bool) -> str:
    """Replace [[Title]] with HTML links or bold text."""
    def replacer(match):
        title = match.group(1)
        if as_bold or title not in title_map:
            return f"**{title}**"
        path = title_map[title]
        return f'[{title}](/wiki/{path})'

    return re.sub(r'\[\[(.+?)\]\]', replacer, text)


_HEBREW_RE = re.compile(r'([\u0590-\u05FF\uFB1D-\uFB4F][\u0590-\u05FF\uFB1D-\uFB4F\s\u0022\u0027\u05F3\u05F4\u05BE"״׳]*[\u0590-\u05FF\uFB1D-\uFB4F\u05F3\u05F4]|[\u0590-\u05FF\uFB1D-\uFB4F])')


def _wrap_hebrew_rtl(html: str) -> str:
    """Wrap Hebrew text runs in <bdi dir="rtl"> tags."""
    return _HEBREW_RE.sub(r'<bdi dir="rtl">\1</bdi>', html)


def parse_article(
    source: str,
    title_map: dict[str, str] | None = None,
    wikilinks_as_bold: bool = False,
) -> tuple[dict, str]:
    """Parse a markdown article with frontmatter.

    Returns (metadata_dict, html_string).
    """
    if title_map is None:
        title_map = {}

    post = frontmatter.loads(source)
    meta = dict(post.metadata)
    body = post.content

    body = _replace_wikilinks(body, title_map, as_bold=wikilinks_as_bold)

    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    html = md.convert(body)

    html = _wrap_hebrew_rtl(html)

    return meta, html
