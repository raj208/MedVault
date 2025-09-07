# search/signals.py
from __future__ import annotations
from django.db import transaction
from django.db.models.signals import post_save, post_delete

from .faiss_store import upsert_doctor_vector, remove_doctor_vector

def _on_doctor_saved(sender, instance, **kwargs):
    """
    After a doctor row is saved, update the FAISS index.
    We wait for the DB commit to succeed before touching the index.
    """
    def _do():
        if getattr(instance, "is_active", True) and getattr(instance, "text_block", ""):
            upsert_doctor_vector(instance.pk, instance.text_block)
        else:
            remove_doctor_vector(instance.pk)

    transaction.on_commit(_do)

def _on_doctor_deleted(sender, instance, **kwargs):
    transaction.on_commit(lambda: remove_doctor_vector(instance.pk))

def bind_doctor_signals(DoctorModel):
    """
    Bind our handlers to whatever Doctor model you're using (settings.DOCTOR_MODEL).
    """
    post_save.connect(
        _on_doctor_saved,
        sender=DoctorModel,
        dispatch_uid="search_doctor_saved_upsert",
        weak=False,
    )
    post_delete.connect(
        _on_doctor_deleted,
        sender=DoctorModel,
        dispatch_uid="search_doctor_deleted_remove",
        weak=False,
    )
