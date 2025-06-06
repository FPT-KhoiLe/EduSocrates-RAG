from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import torch

def embed_chunks(
        chunks: List[str],
        model_name: str = "intfloat/e5-large-v2"
) -> torch.Tensor:
    """
    Encode list of text chunks thành một ma trận embedding.
    Input:
        - chunks: List[str], each element <= vài trăm token
        - model_name: HF repo name cho SentenceTransformer
    Output:
        - embs: np.ndarray shape = (len(chunks), dim)
    """

    model = SentenceTransformer(model_name)
    embs = model.encode(
        chunks,
        convert_to_tensor=True,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
    return embs

def build_faiss_index(
        embs: np.ndarray
) -> faiss.Index:
    """
    Khởi tạo FAISS Index để tìm kNN theo cosine similarity.
    Input:
        - embs: np.ndarray shape = (N, dim), đã L2-normalize
    Output:
        - index: FAISS IndexFlatIP với tất cả vectors đã thêm
    """
    N, dim = embs.shape
    index = faiss.IndexFlatIP(dim)
    index.add(embs)
    return index

def retrieve_top_k(
        index: faiss.Index,
        query_embs: np.ndarray,
        chunks: List[str],
        k: int = 5
) -> List[Tuple[str, float]]:
    """
    Tìm top-k chunks tương tự nhất với query embedding.
    Input:
        - index: FAISS Index built từ embed_chunks
        - query_embs: np.ndarray shape = (1, dim), normalized
        - chunks : List[str], nội dung tương ứng với index
        - k: số lượng trả về
    Output:
        - List of (chunk_text, similarity_score)
    """
    D, I = index.search(query_embs, k)
    results = []
    for idx, score in zip(I[0], D[0]):
        results.append((chunks[idx], score))
    return results

