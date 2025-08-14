from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    # =============================
    #        AUTHENTIFICATION
    # =============================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login-juriste/', views.login_juriste, name='login_juriste'),
    path('login-citoyen/', views.login_citoyen, name='login_citoyen'),

    # =============================
    #        INSCRIPTION
    # =============================
    path('signup/', views.signup_choice, name='signup_choice'),
    path('signup/citoyen/', views.signup_citoyen, name='signup_citoyen'),
    path('signup/juriste/', views.signup_juriste, name='signup_juriste'),
    path('register/juriste/', views.register_juriste, name='register_juriste'),

    # =============================
    #        PROFIL JURISTE
    # =============================
    path('profil/', views.voir_profil, name='voir_profil'),
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),

    # =============================
    #        PROFIL CITOYEN
    # =============================
    path('profil/citoyen/', views.voir_profil_citoyen, name='voir_profil_citoyen'),
    path('modifier-profil/citoyen/', views.modifier_profil_citoyen, name='modifier_profil_citoyen'),

    # =============================
    #        DASHBOARD JURISTE
    # =============================
    path('dashboard/', views.juriste_dashboard, name='juriste_dashboard'),

    # =============================
    #        PAGE D'ACCUEIL
    # =============================
    path('', views.accueil, name='accueil'),
    path('login/citoyen/', views.login_citoyen_view, name='login_citoyen_view'),


    # =============================
    #        DÉTAILS JURISTE
    # =============================
   
]
