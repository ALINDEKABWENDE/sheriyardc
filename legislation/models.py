#from django.db import models
# legislation/models.py
from django.db import models

class TexteLegal(models.Model):
    titre = models.CharField(max_length=255)
    corps = models.TextField()
    domaine = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    date_publication = models.DateField()
    fichier_original = models.FileField(upload_to="lois/")


# Create your models here.
