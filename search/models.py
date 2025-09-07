from django.db import models
from django.utils import timezone

class PatientQueryLog(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=120, blank=True, default="")
    pincode = models.CharField(max_length=10, blank=True, default="")
    languages = models.JSONField(default=list, blank=True)
    raw_text = models.TextField(blank=True, default="")
    topk = models.IntegerField(default=10)
    results = models.JSONField(default=list, blank=True)  # e.g., [{"doctor_id": 7, "score": 0.87}, ...]
