from fastapi import FastAPI
from edusocrates_rag.data_ingest.vector_store import load_index, search
from pathlib import Path
app = FastAPI()
index, meta = load_index(Path("openwebui_data/knowledge/economics"))

@app.get("/search")
def search_api(q: str, k : int = 5):
    return search(q, Path("openwebui_data/knowledge/economics"),k)
