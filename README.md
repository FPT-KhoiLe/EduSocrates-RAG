# EduSocrates-RAG Project Summary

---

## 1. Tên dự án

**EduSocrates-RAG** – Hệ thống hỏi đáp kiểu “Socrates” dành cho sinh viên, chạy hoàn toàn **local** không dùng API, dựa trên phương pháp Retrieval-Augmented Generation (RAG).

---

## 2. Sứ mệnh & Ý nghĩa

- Giúp người học “tự vấn” kiến thức qua đối thoại có dẫn chứng từ giáo trình.  
- Khuyến khích tư duy phản biện thay vì tra cứu đáp án thụ	 động.  
- Hỗ trợ học tập hiệu quả, phù hợp môi trường giáo dục Việt Nam.  

---

## 3. Ý tưởng xuất phát

- Từ trải nghiệm ChatGPT, Khanmigo…  
- Mong muốn xây dựng công cụ AI hướng dẫn theo phong cách Socratic (hỏi gợi mở, không trả lời thẳng).  
- Không phụ thuộc API thương mại, hỗ trợ học tập offline.  
- Tận dụng kỹ thuật RAG để liên tục cập nhật kiến thức từ giáo trình tiếng Việt.

---

## 4. Định nghĩa bài toán

| Thành phần | Mô tả |
|------------|--------|
| **Input** | Bộ tài liệu PDF/PPTX môn Deep Learning + câu hỏi tự do của sinh viên |
| **Output** | Phản hồi theo phong cách Socratic: chuỗi câu hỏi gợi mở, giải thích kèm trích dẫn đoạn text liên quan |

---

## 5. Phạm vi và Mục tiêu

- Tập trung vào giáo trình Deep Learning cơ bản và nâng cao.  
- Xây dựng pipeline ingest tài liệu → chunk → embedding → index FAISS.  
- Fine-tune LLM với LoRA để có phong cách Socratic.  
- Tạo UI demo, API backend phục vụ trải nghiệm người dùng.  
- Đảm bảo chất lượng, hiệu năng (latency < 3s, recall@5 > 70%).

---

## 6. Lộ trình 8 tuần

| Tuần | Nội dung chính                                   | Deliverable                           |
|-------|------------------------------------------------|-------------------------------------|
| 1     | Scaffold repo, CI, test đầu tiên                | Repo, workflow, test import         |
| 2     | Ingest: parse PDF/PPTX, chunk & metadata        | Hàm `ingest_pdf`, chunk nhỏ, test   |
| 3     | Embedding & FAISS index                          | Vector store, retrieval script       |
| 4     | RAG system: retrieval + prompt assembly         | Prompt builder, retrieval API demo   |
| 5     | Data instruction cho LoRA                         | Dataset socratic (prompt-response)  |
| 6     | LoRA fine-tuning                                 | Model adapter weights, training logs |
| 7     | RAG end-to-end pipeline + đánh giá               | Eval metrics, benchmark report       |
| 8     | UI + deploy + báo cáo + pitch deck                | Demo live, báo cáo khoa học          |

---

## 7. Kiến trúc tổng thể

```mermaid
flowchart LR
  subgraph Data Ingestion
    PDF_PPTX --> Chunking --> Embedding --> FAISS_Index
  end

  subgraph RAG Core
    Query --> Query_Embedding --> FAISS_Index
    FAISS_Index --> TopK_Chunks --> Prompt_Assembly --> LLM+LoRA --> Response
  end

  User <--> Response

