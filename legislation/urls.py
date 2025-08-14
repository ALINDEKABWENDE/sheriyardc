# legislation/urls.py
from django.urls import path
from .views import recherche_lois

app_name = 'legislation'  # ✅ obligatoire si tu veux un namespace

urlpatterns = [
    path('recherche-lois/', recherche_lois, name='recherche_lois'),
]
