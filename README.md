# EduSocrates‑RAG

**Fine‑tune LoRA trên Mistral‑7B cho domain Giáo dục, xây dựng hệ thống Socratic Q&A nội bộ (RAG) hỗ trợ sinh viên tự học.**

## Vision

Xây dựng trợ lý học tập AI chạy offline, cho phép sinh viên:
- Tra cứu ngay nội dung trong slide/PDF
- Sinh quiz & flash‑card tự động
- Theo dõi lộ trình học cá nhân hóa

## Scope tuần 1

- Scaffold project structure  
- Viết `requirements.txt`  
- Viết test đơn giản đảm bảo import module `ingest.py`  

## Scope tuần 2
- Viết hàm `parse_pdf` cho `ingest.py`, `pytest` `test_ingest.py` pass xanh.
- `parse_pdf` trả về cấu trúc dạng:
  - List record
    {doc: str,
    chapter: Optional[str],
    page: int,
    text: str}
- Viết hàm `split_sentences(text)`, `make_chunks` để lấy chunks và kết hợp vào pipeline.
## Tech Stack

| Layer       | Thư viện                  |
|-------------|---------------------------|
| Embed/Index | `sentence-transformers`<br/>`faiss-cpu` |
| LLM + LoRA  | `transformers`, `peft`    |
| CLI & API   | `typer`, `FastAPI`        |
| UI demo     | `streamlit`               |
| PDF parsing | `pypdf`                   |
| Test        | `pytest`                  |
