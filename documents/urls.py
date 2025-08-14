from django.urls import path
from . import views  # ✅ Corrigé : import complet des vues

app_name = 'documents'

urlpatterns = [
    path('liste/', views.documents_liste, name='documents_liste'),
    path('upload/', views.upload_document, name='upload_document'),
]

