from django.contrib import admin
from .models import Document, ModeleDocument, DocumentGenere

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_creation')
    search_fields = ('titre', 'contenu', 'auteur__username')
    list_filter = ('date_creation',)

@admin.register(ModeleDocument)
class ModeleDocumentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'date_ajout')
    search_fields = ('nom', 'categorie')
    list_filter = ('categorie',)

@admin.register(DocumentGenere)
class DocumentGenereAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'modele', 'date_creation')
    search_fields = ('utilisateur__username', 'modele__nom')
    list_filter = ('date_creation',)
