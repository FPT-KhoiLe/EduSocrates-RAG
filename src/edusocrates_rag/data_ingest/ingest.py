# src/edusocrates_rag/ingest.py
from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from nltk.tokenize import sent_tokenize
import re

def split_sentences(text: str) -> List[str]:
    # 1. Clean: replace newline with space, remove multi space
    cleaned = re.sub(r"\s+", " ", text).strip()

    # 2. Split sentences
    sentences = sent_tokenize(text)

    return sentences


def make_chunks(
        sentences: List[str],
        max_tokens: int = 500,
        overlap: int = 50,
) -> List[str]:
    chunks = []
    current_chunk = []
    current_len = 0

    for sent in sentences:
        words = sent.split()
        sent_len = len(words)

        # Nếu thêm sent vượt quá mã tokens
        if current_len + sent_len > max_tokens:
            # 1. Xuất chunk hiện tại
            chunks.append(" ".join(current_chunk))

            # 2. Tạo overlap: giữ lại overlap từ cuối chunk
            if overlap > 0:
                # gộp tất cả từ rồi lấy last overlap từ
                tail_words = " ".join(current_chunk[-overlap:]).split()[-overlap:]
                current_chunk = [" ".join(tail_words)]
                current_len = len(tail_words)
            else:
                current_chunk = []
                current_len = 0

        # Thêm sentence vào chunk
        current_chunk.append(sent)
        current_len += sent_len

    # Xuất chunk cuối nếu còn
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def parse_pdf(pdf_path: str) -> List[Dict]:
    """
    Read outline and text page by page from PDF file.
    Return: List record
    {doc: str,
    chapter: Optional[str],
    page: int,
    chunk: int,
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

def ingest_pdf(pdf_path: str, max_tokens=500, overlap=80) -> List[Dict]:
    """
    Parse + chunk PDF, return list of records chunked.
    """
    raw_pages = parse_pdf(pdf_path)
    chunked = []
    for rec in raw_pages:
        sentences = split_sentences(rec["text"])
        chunks = make_chunks(sentences, max_tokens, overlap)
        for idx, text in enumerate(chunks):
            chunked.append({
                **{k: rec[k] for k in ("doc", "chapter", "page")},
                "chunk_id": f"{rec['page']}-{idx}",
                "text": text
            })
    return chunked

