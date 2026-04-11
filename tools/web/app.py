"""Flask wiki browser application."""
import json
import os
from pathlib import Path

from flask import Flask, abort, render_template

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from renderer import build_title_map, parse_article

# Try to import PDF support — optional dependency
try:
    from pdf_export import generate_pdf
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def _find_wiki_root() -> Path:
    """Locate the wiki/ directory via env var or by walking up from this file."""
    env_path = os.environ.get("WIKI_ROOT")
    if env_path:
        return Path(env_path)
    here = Path(__file__).resolve()
    for parent in [here.parent, here.parent.parent, here.parent.parent.parent]:
        candidate = parent / "wiki"
        if candidate.is_dir():
            return candidate
    raise RuntimeError(
        "Cannot find wiki/ directory. "
        "Set the WIKI_ROOT environment variable or use --wiki <path>."
    )


def create_app(wiki_root: Path | None = None) -> Flask:
    if wiki_root is None:
        wiki_root = _find_wiki_root()

    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
    )

    title_map = build_title_map(wiki_root)

    backlinks_file = wiki_root / "_backlinks.json"
    backlinks = {}
    if backlinks_file.exists():
        backlinks = json.loads(backlinks_file.read_text(encoding="utf-8"))

    @app.route("/")
    def index():
        index_file = wiki_root / "_index.md"
        if index_file.exists():
            source = index_file.read_text(encoding="utf-8")
            meta, html = parse_article(source, title_map=title_map)
        else:
            meta, html = {}, "<p>No index file found.</p>"
        return render_template("index.html", content=html, meta=meta, title="Wiki")

    @app.route("/wiki/<path:article_path>")
    def article(article_path: str):
        md_file = wiki_root / f"{article_path}.md"
        if not md_file.exists():
            abort(404)

        source = md_file.read_text(encoding="utf-8")
        meta, html = parse_article(source, title_map=title_map)
        title = meta.get("title", article_path)

        article_backlinks = []
        if title in backlinks:
            for ref_title in backlinks[title].get("referenced_by", []):
                ref_path = title_map.get(ref_title)
                article_backlinks.append({
                    "title": ref_title,
                    "path": f"/wiki/{ref_path}" if ref_path else None,
                })

        return render_template(
            "article.html",
            content=html,
            meta=meta,
            title=title,
            article_path=article_path,
            backlinks=article_backlinks,
            pdf_available=PDF_AVAILABLE,
        )

    if PDF_AVAILABLE:
        @app.route("/wiki/<path:article_path>/pdf")
        def article_pdf(article_path: str):
            md_file = wiki_root / f"{article_path}.md"
            if not md_file.exists():
                abort(404)

            source = md_file.read_text(encoding="utf-8")
            meta, html = parse_article(
                source, title_map=title_map, wikilinks_as_bold=True
            )
            title = meta.get("title", article_path)

            pdf_html = render_template("pdf.html", content=html, meta=meta, title=title)
            pdf_bytes = generate_pdf(pdf_html)

            return pdf_bytes, 200, {
                "Content-Type": "application/pdf",
                "Content-Disposition": f'attachment; filename="{title}.pdf"',
            }

    return app


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Personal Wiki Browser")
    parser.add_argument(
        "--wiki", help="Path to wiki/ directory (or set WIKI_ROOT env var)"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to run on (default: 5000)"
    )
    args = parser.parse_args()

    if args.wiki:
        os.environ["WIKI_ROOT"] = args.wiki

    app = create_app()
    root = Path(os.environ.get("WIKI_ROOT", "")) if os.environ.get("WIKI_ROOT") else _find_wiki_root()
    print(f"  Wiki root : {root}")
    print(f"  PDF export: {'enabled' if PDF_AVAILABLE else 'disabled (pip install xhtml2pdf to enable)'}")
    print(f"  Running at: http://localhost:{args.port}")
    app.run(debug=True, port=args.port)
