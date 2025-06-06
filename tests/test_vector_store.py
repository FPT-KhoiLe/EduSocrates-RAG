# tests/test_vector_store.py

import numpy as np
import pytest
import faiss
from edusocrates_rag.data_ingest.vector_store import embed_chunks, build_faiss_index, retrieve_top_k

def test_embed_chunks_shape_and_norm():
    # 1. Chuẩn bị input: 2 đoạn text cực đơn giản
    texts = ["hello world", "foo bar"]

    # 2. Gọi hàm embed_chunks với model nhỏ gọn (vd. all-MiniLM-L6-v2)
    embs = embed_chunks(texts, model_name="sentence-transformers/all-MiniLM-L6-v2")

    # TODO: Kiểm rằng embs có đúng 2 dòng (2 đoạn)
    assert embs.shape[0] == 2

    # TODO: Tính norms = np.linalg.norm(embs, axis=1) và assert mọi giá trị ≈ 1.0
    norms = np.linalg.norm(embs.cpu().numpy(), axis=1)
    assert np.allclose(norms, 1.0)

def test_build_faiss_index_basic():
    # 1. Tạo ma trận identity 3x3
    eye = np.eye(3, dtype="float32")

    # 2. Xây index
    index = build_faiss_index(eye)

    # TODO: Kiểm rằng index.ntotal == 3
    assert index.ntotal == 3
    # 3. Truy vấn vector đầu tiên (eye[0:1]) với k=1
    D, I = index.search(eye[0:1], 1)

    # TODO: Assert I[0][0] == 0
    assert I[0][0] == 0
    # TODO: Assert D[0][0] ≈ 1.0
    assert np.allclose(D[0][0], 1.0)

def test_retrieve_top_k_simple():
    # 1. Chuẩn bị chunks list và embeddings identity
    chunks = ["a", "b", "c"]
    eye = np.eye(3, dtype="float32")
    index = build_faiss_index(eye)

    # 2. Truy vấn thứ 2 (eye[1:2]), k=2
    results = retrieve_top_k(index, eye[1:2], chunks, k=2)

    # TODO: Assert results là list của 2 tuple
    assert isinstance(results, list)
    assert len(results) == 2
    # TODO: Assert results[0][0] == "b" và results[0][1] == 1.0
    assert results[0][0] == "b" and results[0][1] == 1.0
    # TODO: Assert type của results[1][1] là float
    assert isinstance(results[1][1], np.float32)
