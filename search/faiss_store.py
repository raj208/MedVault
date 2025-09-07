# search/faiss_store.py
from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Tuple

import os
import faiss
import numpy as np
from django.apps import apps
from django.conf import settings
from django.db.models import QuerySet

from .embedding import encode, get_dim

# -----------------------------
# Paths / settings
# -----------------------------
_INDEX_DIR = Path(getattr(settings, "FAISS_DIR", Path(settings.BASE_DIR) / "var" / "faiss"))
_INDEX_DIR.mkdir(parents=True, exist_ok=True)
_INDEX_PATH = _INDEX_DIR / "doctors.index"
_TMP_PATH = _INDEX_DIR / "doctors.index.tmp"

# Allow overriding the Doctor model location (e.g., "myapp.Doctor")
_DOCTOR_LABEL = getattr(settings, "DOCTOR_MODEL", "doctors.Doctor")

# In-process singleton for performance
_INDEX: faiss.Index | None = None


# -----------------------------
# Model access (no hard import)
# -----------------------------
def _DoctorModel():
    """
    Resolve the Doctor model dynamically: avoids hard-coded imports and app init order issues.
    """
    app_label, model_name = _DOCTOR_LABEL.split(".")
    return apps.get_model(app_label, model_name)


# -----------------------------
# Index helpers
# -----------------------------
def _new_index(dim: int) -> faiss.Index:
    """
    Exact cosine search (L2-normalized vectors) using inner product.
    Store 64-bit IDs with IndexIDMap2.
    """
    base = faiss.IndexFlatIP(dim)
    return faiss.IndexIDMap2(base)


def _read_index() -> faiss.Index | None:
    if _INDEX_PATH.exists():
        return faiss.read_index(str(_INDEX_PATH))
    return None


def _write_index_atomic(index: faiss.Index) -> None:
    """
    Atomic write to avoid partial/corrupt index files on crashes.
    """
    faiss.write_index(index, str(_TMP_PATH))
    os.replace(_TMP_PATH, _INDEX_PATH)


def _ensure_dim_compat(idx: faiss.Index) -> faiss.Index:
    """
    If on-disk index dimension mismatches the current encoder dimension, rebuild.
    """
    want = get_dim()
    have = idx.d
    if have != want:
        # Rebuild a fresh (empty) index with correct dimension.
        idx = _new_index(want)
        _write_index_atomic(idx)
    return idx


def load_index() -> faiss.Index:
    """
    Lazy-load the FAISS index.
    If missing or dim-mismatched, create an empty one with correct dim.
    """
    global _INDEX
    if _INDEX is not None:
        return _INDEX

    idx = _read_index()
    if idx is None:
        idx = _new_index(get_dim())
        _write_index_atomic(idx)
    else:
        idx = _ensure_dim_compat(idx)

    _INDEX = idx
    return _INDEX


# -----------------------------
# Data streaming from Postgres
# -----------------------------
def _iter_active_doctors(batch_size: int = 512) -> Iterable[Tuple[int, str]]:
    """
    Stream (pk, text_block) for active doctors.
    Uses pk because your model's PK is the OneToOne (not 'id').
    """
    Doctor = _DoctorModel()
    qs: QuerySet = (
        Doctor.objects
        .filter(is_active=True)
        .order_by("pk")
        .values_list("pk", "text_block")
    )
    for pk, text in qs.iterator(chunk_size=batch_size):
        yield int(pk), (text or "")


# -----------------------------
# Build / Rebuild
# -----------------------------
def rebuild_index(batch_size: int = 512) -> faiss.Index:
    """
    Rebuild the full index from Postgres (active doctors only).
    """
    ids: List[int] = []
    chunks: List[str] = []
    vecs: List[np.ndarray] = []

    for pk, text in _iter_active_doctors(batch_size=batch_size):
        ids.append(pk)
        chunks.append(text)
        if len(chunks) >= batch_size:
            vecs.append(encode(chunks))
            chunks.clear()

    if chunks:
        vecs.append(encode(chunks))

    dim = get_dim()
    index = _new_index(dim)

    if vecs:
        X = np.vstack(vecs).astype("float32")   # (N, d)
        I = np.array(ids, dtype="int64")        # doctor PKs
        index.add_with_ids(X, I)

    _write_index_atomic(index)

    # refresh singleton
    global _INDEX
    _INDEX = index
    return index


# -----------------------------
# Search / Upsert / Remove
# -----------------------------
def search_knn(query_text: str, topk: int = 50) -> List[Tuple[int, float]]:
    """
    Embed query (normalized) and return [(doctor_pk, similarity), ...].
    """
    index = load_index()
    if index.ntotal == 0:
        return []

    q = encode([query_text])  # (1, d)
    D, I = index.search(q, topk)
    out: List[Tuple[int, float]] = []
    for pk, sim in zip(I[0].tolist(), D[0].tolist()):
        if pk != -1:
            out.append((int(pk), float(sim)))
    return out


def upsert_doctor_vector(doctor_pk: int, text_block: str) -> None:
    """
    Incremental update: remove old vector for PK (if any), then add new one.
    """
    index = load_index()

    # Remove existing vector for this PK (no-op if absent)
    sel = faiss.IDSelectorBatch(np.array([doctor_pk], dtype="int64"))
    index.remove_ids(sel)

    # Add new vector
    v = encode([text_block]).astype("float32")  # (1, d)
    index.add_with_ids(v, np.array([doctor_pk], dtype="int64"))

    _write_index_atomic(index)


def remove_doctor_vector(doctor_pk: int) -> None:
    """
    Remove a doctor from the index (deactivated/deleted).
    """
    index = load_index()
    sel = faiss.IDSelectorBatch(np.array([doctor_pk], dtype="int64"))
    index.remove_ids(sel)
    _write_index_atomic(index)
