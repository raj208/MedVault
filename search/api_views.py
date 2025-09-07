from __future__ import annotations
from typing import Any, Dict, List

from django.apps import apps
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .faiss_store import search_knn
from .rerank import rerank

_DOCTOR_LABEL = getattr(settings, "DOCTOR_MODEL", "doctors.Doctor")

def _DoctorModel():
    app_label, model_name = _DOCTOR_LABEL.split(".")
    return apps.get_model(app_label, model_name)

class SearchView(APIView):
    """
    POST /api/search
    {
      "symptoms": "chest pain, shortness of breath",
      "history": "diabetes",
      "city": "Mumbai",
      "pincode": "400001",
      "languages": ["en", "hi"],
      "topk": 10
    }
    """
    def post(self, request, *args, **kwargs):
        data: Dict[str, Any] = request.data or {}

        symptoms = str(data.get("symptoms", "") or "").strip()
        history = str(data.get("history", "") or "").strip()
        city = str(data.get("city", "") or "").strip()
        pincode = str(data.get("pincode", "") or "").strip()
        languages = data.get("languages") or []
        if not isinstance(languages, list):
            return Response({"error": "languages must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            topk = int(data.get("topk"))
        except Exception:
            return Response({"error": "topk is required and must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Clamp topk to reasonable bounds
        topk = max(1, min(50, topk))

        # Build query text for semantic retrieval
        query_text = f"Symptoms: {symptoms}\nHistory: {history}".strip()

        # Over-fetch to give reranker room (x5 is a decent default)
        initial = search_knn(query_text, topk=topk * 5)
        if not initial:
            return Response({"results": []}, status=status.HTTP_200_OK)

        id_to_sim = {pk: sim for pk, sim in initial}
        ids = [pk for pk, _ in initial]

        Doctor = _DoctorModel()
        docs = list(Doctor.objects.filter(pk__in=ids, is_active=True))

        patient = {
            "symptoms": symptoms,
            "history": history,
            "city": city,
            "pincode": pincode,
            "languages": languages,
        }

        ranked = rerank(patient, docs, id_to_sim)[:topk]

        results = []
        for r in ranked:
            d = r["doctor"]
            results.append({
                "doctor_id": d.pk,
                "name": getattr(d, "name", ""),
                "specialties": getattr(d, "specialties", []),
                "yoe": getattr(d, "years_of_experience", 0),
                "hospital": getattr(d, "hospital", ""),
                "city": getattr(d, "city", ""),
                "pincode": getattr(d, "pincode", ""),
                "languages": getattr(d, "languages", []),
                "phone": getattr(d, "phone", ""),
                "email": getattr(d, "email", ""),
                "score": round(float(r["score"]), 4),
            })

        return Response({"results": results}, status=status.HTTP_200_OK)
