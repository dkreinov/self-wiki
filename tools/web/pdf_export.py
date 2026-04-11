"""PDF generation using xhtml2pdf.

Install the optional dependency to enable:
    pip install xhtml2pdf
"""
import io

from xhtml2pdf import pisa


def generate_pdf(html: str) -> bytes:
    """Convert an HTML string to PDF bytes."""
    buf = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buf)
    if pisa_status.err:
        raise RuntimeError(f"PDF generation failed with {pisa_status.err} errors")
    return buf.getvalue()
