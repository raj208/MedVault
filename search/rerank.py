# search/rerank.py
from __future__ import annotations
from typing import Dict, List, Any
from .ontology import get_ontology

# Weights (fixed by your policy)
W_SPEC = 0.55
W_PROX = 0.25
W_YOE  = 0.15
W_LANG = 0.05

def _norm_yoe(values: List[int]) -> Dict[int, float]:
    if not values:
        return {}
    mn, mx = min(values), max(values)
    if mx <= mn:
        # all equal or empty range -> zero contribution
        return {v: 0.0 for v in values}
    return {v: (v - mn) / (mx - mn) for v in values}

def _proximity_score(p_city: str, p_pin: str, d_city: str, d_pin: str) -> float:
    # Simple baseline (no lat/lon yet):
    if p_pin and d_pin and p_pin == d_pin:
        return 1.0
    if p_city and d_city and p_city.strip().lower() == d_city.strip().lower():
        return 0.6
    return 0.0

def _language_score(p_langs: List[str], d_langs: List[str]) -> float:
    try:
        return 1.0 if set(p_langs or []) & set(d_langs or []) else 0.0
    except Exception:
        return 0.0

def rerank(patient: Dict[str, Any], doctors: List[Any], id_to_sim: Dict[int, float]) -> List[Dict[str, Any]]:
    """
    patient = {"symptoms","history","city","pincode","languages"}
    doctors = list of Doctor instances
    id_to_sim = {pk: faiss_similarity}  # kept for debugging; not used in score
    returns list of {doctor, score, faiss_sim} sorted desc
    """
    onto = get_ontology()
    inferred = onto.infer_from_text(patient.get("symptoms",""), patient.get("history",""))

    # Precompute YOE normalization over the candidate set
    y_values = [getattr(d, "years_of_experience", 0) or 0 for d in doctors]
    y_norm_map = _norm_yoe(y_values)

    out = []
    for d in doctors:
        spec = onto.score(inferred, getattr(d, "specialties", []) or [])
        prox = _proximity_score(patient.get("city",""), patient.get("pincode",""),
                                getattr(d, "city",""), getattr(d, "pincode",""))
        yoe_raw = getattr(d, "years_of_experience", 0) or 0
        y = y_norm_map.get(yoe_raw, 0.0)
        lang = _language_score(patient.get("languages", []), getattr(d, "languages", []) or [])

        score = W_SPEC*spec + W_PROX*prox + W_YOE*y + W_LANG*lang
        out.append({
            "doctor": d,
            "score": float(score),
            "faiss_sim": float(id_to_sim.get(d.pk, 0.0)),
        })

    out.sort(key=lambda x: x["score"], reverse=True)
    return out
