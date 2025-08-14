# actualites/urls.py
from django.urls import path
from . import views

app_name = 'actualites'

urlpatterns = [
    path('', views.voir_actualites, name='liste_actualites'),
    path('vue/', views.actualites_view, name='actualites_view'),
    path('article/<int:article_id>/', views.article_detail_view, name='detail_article'),
]
