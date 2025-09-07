from django.urls import path
from .api_views import SearchView

urlpatterns = [
    path("search", SearchView.as_view(), name="api_search"),
]
