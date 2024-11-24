from pathlib import Path 
import os
 
# Build paths inside the project like this: BASE_DIR / 'subdir'. 
BASE_DIR = Path(__file__).resolve().parent.parent 
 
# SECURITY WARNING: keep the secret key used in production secret! 
SECRET_KEY = 'django-insecure-33#4ps66k*$#xr0p-%2)-((h^-2l0!9j^z3-j_ow4+(j84p+)$' 
 
# SECURITY WARNING: don't run with debug turned on in production! 
DEBUG = True 
 
ALLOWED_HOSTS = [] 
 
# Application definition 
INSTALLED_APPS = [ 
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles',
    
    'rest_framework',
    'corsheaders',
    
    'anime',  # Заменил 'games' на 'anime'
] 
 
MIDDLEWARE = [ 
    'corsheaders.middleware.CorsMiddleware',  # Добавил CORS middleware
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
] 

# Добавил CORS настройки
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CORS_ALLOW_CREDENTIALS = True
 
ROOT_URLCONF = 'config.urls'  # Изменил 'app.urls' на 'config.urls'
 
TEMPLATES = [ 
    { 
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [ 
            BASE_DIR / "templates" 
        ], 
        'APP_DIRS': True, 
        'OPTIONS': { 
            'context_processors': [ 
                'django.template.context_processors.debug', 
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth', 
                'django.contrib.messages.context_processors.messages', 
            ], 
        }, 
    }, 
] 
 
WSGI_APPLICATION = 'config.wsgi.application'  # Изменил 'app.wsgi' на 'config.wsgi'
 
DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': BASE_DIR / 'db.sqlite3', 
    } 
} 
 
AUTH_PASSWORD_VALIDATORS = [ 
    { 
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', 
    }, 
    { 
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 
    }, 
    { 
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', 
    }, 
    { 
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', 
    }, 
] 
 
LANGUAGE_CODE = 'en-us' 
 
TIME_ZONE = 'UTC' 
 
USE_I18N = True 
 
USE_TZ = True 
 
STATIC_URL = 'static/' 
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'