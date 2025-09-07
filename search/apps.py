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


