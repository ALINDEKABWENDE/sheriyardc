from rest_framework import serializers, viewsets
from .models import RendezVous, Question, Réponse, AppelVideo

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '__all__'

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
