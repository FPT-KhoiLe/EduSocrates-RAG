# src/edusocrates_rag/ingest.py
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader

def split_sentences(text: str) -> List[str]:
    return text.split(".")

def parse_pdf(pdf_path: str) -> List[Dict]:
    """
    Read outline and text page by page from PDF file.
    Return: List record
    {doc: str,
    chapter: Optional[str],
    page: int,
    text: str}
    """
    path = Path(pdf_path)
    reader = PdfReader(path)

    # 1. Get outline (if available), build list[(title, page_num)]
    outline = []
    try:
        for dest in reader.outline:
            # dest: Destination object
            title = dest.title
            page_num = reader.get_destination_page_number(dest) + 1
            outline.append((title, page_num))
    except Exception:
        outline = []

    records = []
    # 2. Go through each page, find nearest heading
    current_chapter = None
    for i, page in enumerate(reader.pages, start=1):
        # Update chapter if meet in outline
        for title, pg in outline:
            if pg == i:
                current_chapter = title
        raw = page.extract_text() or ""
        records.append({
            "doc": path.stem,
            "chapter": current_chapter,
            "page": i,
            "text": raw,
        })
    return records