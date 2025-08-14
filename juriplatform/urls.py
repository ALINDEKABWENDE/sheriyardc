from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view  # ✅ Import direct pour /login

urlpatterns = [
    # 🛠️ Interface d’administration
    path('admin/', admin.site.urls),

    # 🧩 Inclusions des apps avec namespace
    path('dossiers/', include('dossiers.urls', namespace='dossiers')),
    path('legislation/', include('legislation.urls', namespace='legislation')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('documents/', include('documents.urls', namespace='documents')),
    path('actualites/', include('actualites.urls', namespace='actualites')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('admin/', admin.site.urls),
    path('consultation/', include('consultation.urls')),  
    path('legislation/', include('legislation.urls')),  # ← inclusion
    



    # 🏛️ Accueil institutionnel
    path('', include('cabinet.urls', namespace='cabinet')),  # ✅ Ajout du namespace pour cohérence

    # 🔐 Authentification / Déconnexion
    path('login/', login_view, name='login'),  # ✅ Corrige l’erreur 404
    path('logout/', LogoutView.as_view(next_page='cabinet:accueil'), name='logout'),  # ✅ Redirection explicite
]

# 🖼️ Fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
