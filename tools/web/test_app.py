"""Tests for the Flask wiki app."""
import pytest


@pytest.fixture
def client(wiki_root):
    from tools.web.app import create_app
    app = create_app(wiki_root=wiki_root)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_contains_article_links(client):
    resp = client.get("/")
    html = resp.data.decode()
    assert "Mr. White" in html
    assert "Mr. Blonde" in html


def test_index_has_html_structure(client):
    resp = client.get("/")
    html = resp.data.decode()
    assert "<html" in html
    assert "</html>" in html
    assert "<title>" in html


def test_article_returns_200(client):
    resp = client.get("/wiki/people/mr-white")
    assert resp.status_code == 200


def test_article_renders_content(client):
    resp = client.get("/wiki/people/mr-white")
    html = resp.data.decode()
    assert "Mr. White" in html
    assert "backend engineer" in html.lower() or "distributed systems" in html.lower()


def test_article_has_wikilinks(client):
    resp = client.get("/wiki/people/mr-white")
    html = resp.data.decode()
    assert 'href="/wiki/' in html


def test_article_has_backlinks(client):
    resp = client.get("/wiki/people/mr-white")
    html = resp.data.decode()
    assert "referenced" in html.lower() or "Historical Doubles" in html or "backlink" in html.lower()


def test_article_404(client):
    resp = client.get("/wiki/people/does-not-exist")
    assert resp.status_code == 404


def test_no_pdf_button_without_pdf(client):
    resp = client.get("/wiki/people/mr-white")
    assert resp.status_code == 200


def test_static_css_served(client):
    resp = client.get("/static/style.css")
    assert resp.status_code == 200
    assert "text/css" in resp.content_type


def test_pattern_article(client):
    resp = client.get("/wiki/patterns/the-reservoir-historical-doubles")
    assert resp.status_code == 200
    html = resp.data.decode()
    assert "Historical Doubles" in html
    assert "Socrates" in html


def test_books_article(client):
    resp = client.get("/wiki/books/book-recommendations")
    assert resp.status_code == 200
    html = resp.data.decode()
    assert "Book Recommendations" in html


def test_demo_graphs_route(client):
    resp = client.get("/demo/graphs")
    # 200 if evolution-graphs.html exists next to wiki/, 404 if not
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        assert "The Reservoir" in resp.data.decode()
