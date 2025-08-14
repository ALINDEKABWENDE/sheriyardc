from pathlib import Path
import os

# 📁 Répertoire de base
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Sécurité
SECRET_KEY = 'django-insecure-7*8@q)7fp_+!ia$w@4z9sl%b@l*5^su8l2k=lgp3@182)e6o3k'
DEBUG = True
ALLOWED_HOSTS = ['*']

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"

# ⚙️ Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'actualites.apps.ActualitesConfig',
    'documents.apps.DocumentsConfig',
    'legislation.apps.LegislationConfig',
    'dossiers.apps.DossiersConfig',
    'cabinet.apps.CabinetConfig',
    'accounts.apps.AccountsConfig',
    'channels',
    'consultation.apps.ConsultationConfig',
     'widget_tweaks',
    'chat',  
]

# 🧱 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ASGI_APPLICATION = "juriplatform.asgi.application"

# Redis pour gérer les connexions WebSocket
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
            
        },
    },
}

# 🌐 Configuration des URLs
ROOT_URLCONF = 'juriplatform.urls'

# 🎨 Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🔧 Application WSGI
WSGI_APPLICATION = 'juriplatform.wsgi.application'

# 🗄️ Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internationalisation
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Kinshasa'
USE_I18N = True
USE_TZ = True

# 📦 Fichiers statiques
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 🆔 Clé primaire automatique
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# —————————————————————
# 🖼️ Fichiers médias (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
