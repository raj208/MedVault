from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import yaml
from django.conf import settings

_WORD = re.compile(r"[A-Za-z][A-Za-z\- ]{1,}")

class SpecialtyOntology:
    """
    Loads a lightweight taxonomy and provides:
      - infer_patient_specialties(symptoms+history)
      - score(patient_labels, doctor_labels) with hierarchy-aware logic
    """
    def __init__(self, data: Dict):
        # Normalize parents -> children
        self.parent_to_children: Dict[str, Set[str]] = {}
        self.child_to_parent: Dict[str, str] = {}
        self.labels: Set[str] = set()

        for parent, children in (data.get("specialties") or {}).items():
            p = parent.strip()
            self.labels.add(p)
            self.parent_to_children.setdefault(p, set())
            for c in children or []:
                c = c.strip()
                self.labels.add(c)
                self.parent_to_children[p].add(c)
                self.child_to_parent[c] = p

        # Synonyms: token -> list of labels
        self.synonyms: Dict[str, Set[str]] = {}
        for token, lbls in (data.get("synonyms") or {}).items():
            self.synonyms[token.lower().strip()] = {l.strip() for l in lbls}

        # Lowercase map for quick text matching
        self._label_lc = {l.lower(): l for l in self.labels}

    @classmethod
    def from_yaml(cls, path: Path) -> "SpecialtyOntology":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(data)

    def infer_from_text(self, symptoms: str, history: str) -> List[str]:
        """
        Simple lexical inference: match labels & synonyms as whole-word-ish substrings.
        """
        text = f"{symptoms or ''} {history or ''}".lower()
        found: Set[str] = set()

        # Label match
        for lc, canon in self._label_lc.items():
            if lc and lc in text:
                found.add(canon)

        # Synonym match
        for token, targets in self.synonyms.items():
            if token in text:
                found.update(targets)

        # Normalize: if child found and parent also present, keep both (doesn't hurt)
        return sorted(found)

    def score(self, patient_labels: List[str], doctor_labels: List[str]) -> float:
        """
        Hierarchical scoring:
          - exact overlap -> 1.0
          - parent<->child -> 0.7
          - siblings under the same parent -> 0.5
          - else -> 0.0
        """
        if not patient_labels or not doctor_labels:
            return 0.0

        pset = set(patient_labels)
        dset = set(doctor_labels)

        # Exact
        if pset & dset:
            return 1.0

        # Parent-child in either direction
        for a in pset:
            for b in dset:
                if self.child_to_parent.get(a) == b or self.child_to_parent.get(b) == a:
                    return 0.7

        # Siblings
        for a in pset:
            pa = self.child_to_parent.get(a)
            if not pa:
                continue
            for b in dset:
                if self.child_to_parent.get(b) == pa:
                    return 0.5

        return 0.0


# Singleton loader
def get_ontology() -> SpecialtyOntology:
    # Allow override; default config path
    ypath = getattr(settings, "SPECIALTY_ONTOLOGY_PATH", None)
    if ypath is None:
        ypath = Path(settings.BASE_DIR) / "config" / "specialty_ontology.yml"
    return SpecialtyOntology.from_yaml(Path(ypath))
