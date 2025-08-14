from django.urls import path, include

urlpatterns = [

    path(
        'juriste/',
        include(('consultation.urls.juriste_urls', 'juriste'), namespace='juriste')
    ),
    path('citoyen/', include('consultation.urls.citoyen_urls')),  
]
