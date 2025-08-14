# consultation/urls/__init__.py
from django.urls import path, include

urlpatterns = [
    path(
        'citoyen/',
        include(('consultation.urls.citoyen_urls', 'citoyen'), namespace='citoyen')
    ),
    path(
        'juriste/',
        include(('consultation.urls.juriste_urls', 'juriste'), namespace='juriste')
    ),
]