from django.urls import path
from consultation.views import juriste

app_name = 'juriste'  # ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ✅

urlpatterns = [
    path('dashboard/', juriste.dashboard_juriste, name='dashboard'),
]
