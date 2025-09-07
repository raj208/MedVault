# MedVault

A secure, user‑friendly platform for storing, managing, and sharing medical records digitally. MedVault lets patients upload prescriptions, lab reports, and other health documents, access them anytime, and share with doctors when needed — with privacy and encryption built in.


## Architecture Overview
```text
 ┌──────────┐        HTTPS        ┌────────────────┐
 │  Client  │  ─────────────────▶ │  Django App    │
 │ (Web UI) │ ◀─────────────────  │  (REST + UI)   │
 └──────────┘     (Templates)     └──────┬─────────┘
                                         │
         ┌───────────────────────────────┼──────────────────────────────┐
         │                               │                              │
 ┌───────────────┐               ┌───────────────┐              ┌────────────────┐
 │  OCR Service  │               │ Summarizer    │              │ Doctor Reco     │
 │ (PaddleOCR)   │               │ (GPT API)     │              │ (BioBERT+FAISS) │
 └──────┬────────┘               └──────┬────────┘              └───────┬─────────┘
        │                               │                                 │
 ┌──────▼────────┐               ┌──────▼────────┐               ┌───────▼─────────┐
 │  Object Store │               │   Postgres    │               │     FAISS Index  │
 │ (S3 / local)  │               │  (metadata)   │               │  (doctor vectors)│
 └───────────────┘               └───────────────┘               └──────────────────┘
```

---

## Tech Stack
**Backend:** Django (Python 3.10+), Django REST Framework  
**DB:** PostgreSQL (production), SQLite (dev only)  
**Search/ANN:** FAISS  
**NLP/Embeddings:** BioBERT (`dmis-lab/biobert-base-cased-v1.1`)  
**OCR:** PaddleOCR  
**LLM:** OpenAI GPT API (configurable)  
**Storage:** AWS S3 (prod) / local media (dev)  
**Infra:** AWS (EC2/Elastic Beanstalk), CloudFront (optional), Nginx/Gunicorn

---

### Local Setup
```bash
# 1) Clone
git clone https://github.com/<you>/MedVault.git
cd MedVault

# 2) Create venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt
```


## Core Modules

### Authentication & Identity
- Standard Django auth (sessions/DRF tokens/JWT as configured).
- **Tokenized/virtual IDs** for users within internal services to minimize exposure of real PII.

### Document Ingestion & Storage
- Upload PDFs/images via UI or API.
- Files stored under `MEDIA_ROOT` (dev) or **S3** (prod).  
- Metadata (owner, file type, language, timestamps) stored in Postgres.

### OCR Extraction (PaddleOCR)
- Extracts text from scanned reports and images.
- Configurable languages via `PADDLE_OCR_LANG`.

### LLM Summarization
- Summarizes extracted text using GPT API to generate patient‑friendly insights.
- Includes **medical disclaimer** (not a diagnosis) in responses.

### Doctor Recommendation Engine (BioBERT + FAISS)
- **Embedding**: Convert symptoms/history text into BioBERT vectors (dimension 768).
- **Retrieval**: FAISS index for nearest doctors.
- **Re‑ranking** with weights (example):
  
  `score = 0.55*specialty_match + 0.25*location_proximity + 0.15*years_experience_norm + 0.05*language_match`
  
- Supports filters: city/pincode, languages.

**Indexing workflow (example):**
```bash
# If you have management commands (recommended):
python manage.py build_doctor_embeddings
python manage.py build_faiss_index --out $FAISS_INDEX_PATH
```
If not, you can prototype in Django shell:
```py
from recommender.embed import embed_doctors  # your module
from recommender.index import build_index     # your module
vecs, meta = embed_doctors()
build_index(vecs, meta, out_path="./data/faiss/doctor_index.faiss")
```

### Consent & Sharing
- Patient-controlled, time‑limited share links.
- Optional one‑time access tokens; downloads require explicit consent.

### Audit Logging
- Immutable audit trail for access, downloads, and shares (model/table `audit_log`).

---

## API Reference (REST)
Base URL: `/api/`

### 1) Upload Document
**POST** `/api/docs/upload`  
`multipart/form-data`: `file`, `doc_type` (e.g., `prescription|labs|report`), `language_mode`
```bash
curl -X POST http://127.0.0.1:8000/api/docs/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/report.pdf" \
  -F "doc_type=labs" -F "language_mode=en"
```
**Response** `201`:
```json
{
  "id": 123,
  "filename": "report.pdf",
  "owner": 42,
  "doc_type": "labs",
  "created_at": "2025-09-08T05:30:00Z"
}
```

### 2) Summarize Document
**POST** `/api/summary`
```json
{
  "document_id": 123,
  "style": "patient_friendly"
}
```
**Response** `200`:
```json
{
  "summary": "This report shows...",
  "highlights": ["HbA1c elevated"],
  "meds": ["Metformin"],
  "followups": ["Consult endocrinologist"],
  "disclaimer": "This is not a medical diagnosis."
}
```

### 3) Doctor Search / Recommendation
**POST** `/api/search`
```json
{
  "symptoms": "chest pain, shortness of breath",
  "history": "diabetes",
  "city": "Mumbai",
  "pincode": "400001",
  "languages": ["en", "hi"],
  "topk": 5
}
```
**Response** `200`:
```json
{
  "results": [
    {
      "doctor_id": 987,
      "name": "Dr. A",
      "specialty": "Cardiology",
      "city": "Mumbai",
      "years_experience": 12,
      "languages": ["en", "hi"],
      "score": 0.87,
      "why": {
        "specialty": 1.0, "proximity": 0.9, "experience": 0.7, "language": 1.0
      }
    }
  ]
}
```

---

**High‑level steps:**
1. Build artifact: `pip install -r requirements.txt`.
2. Set env vars in EB/EC2 (use SSM).
3. Ensure `USE_S3=true` and bucket/region configured.
4. Run `python manage.py migrate && python manage.py collectstatic`.
5. Warm up OCR/LLM; build or upload FAISS index.


