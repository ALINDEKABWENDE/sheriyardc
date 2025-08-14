from django.contrib import admin
from .models import ArticleActualite

@admin.register(ArticleActualite)
class ArticleActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'date_publication')
    search_fields = ('titre', 'contenu', 'auteur', 'categorie')
    list_filter = ('categorie', 'date_publication')
