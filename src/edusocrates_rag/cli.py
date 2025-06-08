import argparse
from pathlib import Path

from edusocrates_rag.data_ingest.ingest import ingest_pdf
from edusocrates_rag.data_ingest.vector_store import build_index

def main():
    p = argparse.ArgumentParser(description="Ingest PDFs/PPTX into Knowledge Base")
    p.add_argument(
        "--in",
        dest="in_files",
        nargs="+",
        required=True,
        help="path(s) to PDF/PPTX"
    )
    p.add_argument(
        "--kb",
        required=True,
        help="knowledge Base name (folder under openwebui_data/knowledge/)"
    )
    p.add_argument(
        "--root",
        default="openwebui_data/knowledge",
        help="root folder that Open_WebUI mounts"
    )
    args = p.parse_args()

    all_chunks = []
    for f in args.in_files:
        all_chunks.extend(ingest_pdf(f))

    kb_path = Path(args.root) / args.kb / "source"
    build_index(all_chunks, kb_path.parent) # index next to 'source'

    # dump text chunks line-by-line for WebUI
    kb_path.mkdir(parents=True, exist_ok=True)
    out_txt = kb_path / "chunks.txt"
    with open(out_txt, "w") as f:
        for chunk in all_chunks:
            f.write(chunk["text"] + "\n")

    print(f"📄🔧 Wrote chunks text → {out_txt}")


if __name__ == "__main__":
    main()