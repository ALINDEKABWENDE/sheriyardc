from django.shortcuts import render, get_object_or_404
from actualites.models import ArticleActualite

# 📰 Vue principale : liste complète des actualités
def voir_actualites(request):
    actualites = ArticleActualite.objects.order_by('-date_publication')
    return render(request, 'actualites/actualites.html', {
        'actualites': actualites
    })

# 🗂️ Vue alternative : affichage différent (template liste.html ou usage contextuel)
def actualites_view(request):
    actualites = ArticleActualite.objects.order_by('-date_publication')
    return render(request, 'actualites/liste.html', {
        'actualites': actualites
    })

# 🧾 Vue pour afficher le détail d’un article
def article_detail_view(request, article_id):
    article = get_object_or_404(ArticleActualite, id=article_id)
    return render(request, 'actualites/article_detail.html', {
        'article': article
    })
