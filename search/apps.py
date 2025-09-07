from django.apps import AppConfig

class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

    def ready(self):
        # Eager load (optional). Comment out if you prefer lazy.
        try:
            from .faiss_store import load_index
            load_index()
        except Exception:
            # Avoid crashing startup—index can be built via management command.
            pass


# search/apps.py
from django.apps import AppConfig, apps
from django.conf import settings

class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

    def ready(self):
        # Resolve the Doctor model dynamically, then bind signals.
        label = getattr(settings, "DOCTOR_MODEL", "doctors.Doctor")
        app_label, model_name = label.split(".")
        DoctorModel = apps.get_model(app_label, model_name)

        from .signals import bind_doctor_signals
        bind_doctor_signals(DoctorModel)

        # Optional: eager-load an empty or on-disk FAISS index so the first query is warm.
        try:
            from .faiss_store import load_index
            load_index()
        except Exception:
            # Keep startup resilient; you can rebuild with the management command.
            pass
