from django.urls import path
from .views import accueil
app_name = 'cabinet'
urlpatterns = [
    path('', accueil, name='accueil'),
]