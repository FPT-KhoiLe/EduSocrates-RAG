# tests/test_ingest.py
import pytest

def test_ingest_importable():
    """
    Đảm bảo import được module và class/function placeholder không lỗi.
    """
    try:
        import edusocrates_rag.ingest as ingest
    except ImportError as e:
        pytest.skip(f"Module ingest chưa hoàn thiện: {e}")
    # Placeholder: ingest.py đã có function chunk_pdf?
    assert hasattr(ingest, "parse_pdf"), "Bạn hãy định nghĩa function parse_pdf()"



def test_parse_pdf_minimal(tmp_path):
    from edusocrates_rag.ingest import parse_pdf

    # Use fake PDF with 1 page, "Hello World" content
    from reportlab.pdfgen import canvas
    pdf_file = tmp_path / "hello.pdf"
    c = canvas.Canvas(str(pdf_file))
    c.drawString(100, 100, "Hello World")
    c.showPage()
    c.save()

    records = parse_pdf(str(pdf_file))

    assert isinstance(records, list), "parse_pdf must return a list"
    assert len(records) == 1, "parse_pdf must return a list with 1 record"
    rec = records[0]
    assert rec["doc"] == "hello", "doc must be the filename without extension"
    assert rec["chapter"] is None, "chapter must be None if not in outline"
    assert rec["page"] == 1, "page must be 1"
    assert rec["text"] == "Hello World\n", "text must be the page content"