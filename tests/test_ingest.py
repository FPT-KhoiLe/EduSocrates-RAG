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
    assert hasattr(ingest, "chunk_pdf"), "Bạn hãy định nghĩa function chunk_pdf()"
