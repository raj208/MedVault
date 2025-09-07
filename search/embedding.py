# search/embedding.py
from __future__ import annotations
from typing import List
import numpy as np
from django.conf import settings

_MODEL = None
_DIM = None

def _load_model():
    """
    Lazy-load a lightweight biomedical sentence-transformer on CPU.
    Falls back to a general MiniLM if the primary model is unavailable.
    """
    global _MODEL, _DIM
    if _MODEL is not None:
        return _MODEL

    from sentence_transformers import SentenceTransformer

    primary = getattr(settings, "EMBED_MODEL", "pritamdeka/S-BioBERT-MiniLM-L6-v2")
    fallback = getattr(settings, "EMBED_FALLBACK", "sentence-transformers/all-MiniLM-L6-v2")

    try:
        _MODEL = SentenceTransformer(primary, device="cpu")
    except Exception:
        _MODEL = SentenceTransformer(fallback, device="cpu")

    # probe once to cache dimensionality
    vec = _MODEL.encode(["probe"], normalize_embeddings=True, convert_to_numpy=True)
    global _DIM
    _DIM = int(vec.shape[1])
    return _MODEL

def get_dim() -> int:
    if _DIM is None:
        _load_model()
    return _DIM

def encode(texts: List[str], batch_size: int = 256) -> np.ndarray:
    """
    Returns L2-normalized float32 vectors (shape: [n, d]).
    Cosine similarity == dot product thanks to normalization.
    """
    model = _load_model()
    # Replace None/empty with whitespace to avoid model edge cases
    safe_texts = [(t if (t is not None and str(t).strip()) else " ") for t in texts]
    emb = model.encode(
        safe_texts,
        batch_size=batch_size,
        normalize_embeddings=True,     # returns unit-length vectors
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype("float32")

    # Extra guard: re-normalize (no-op if already unit)
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12
    emb = emb / norms
    return emb
