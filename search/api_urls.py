from django.urls import path
from .api_views import SearchView
from .views import search_test_page

urlpatterns = [
    path("search", SearchView.as_view(), name="api_search"),
    path("search/test", search_test_page, name="search_test_page"),  # simple UI
]
