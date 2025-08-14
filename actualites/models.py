from django.db import models

class ArticleActualite(models.Model):
    titre = models.CharField("Titre", max_length=200)
    contenu = models.TextField("Contenu")
    auteur = models.CharField("Auteur", max_length=100)
    date_publication = models.DateTimeField("Date de publication", auto_now_add=True)
    categorie = models.CharField("Catégorie", max_length=100)
    image = models.ImageField("Image illustratrice", upload_to='actualites/', null=True, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.categorie})"

    class Meta:
        verbose_name = "Article d'actualité"
        verbose_name_plural = "Articles d'actualités"
        ordering = ['-date_publication']
