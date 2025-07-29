import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
FERNET_KEY = os.getenv('FERNET_KEY')
DEBUG = os.getenv('DEBUG') == '1'
ALLOWED_HOSTS = ['*']


FIELD_ENCRYPTION_KEY=[FERNET_KEY]


APPEND_SLASH = False

APIS = {
    'ZAP_SIGN': os.getenv('ZAP_SIGN_API_URL', 'https://api.zapsign.com.br'),
    'ZAP_SIGN_APP': os.getenv('ZAP_SIGN_APP_URL', 'https://sandbox.app.zapsign.com.br'),
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs de terceiros
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_eventstream',
    'django_cryptography',
    'infrastructure.apps.InfrastructureConfig',
    'corsheaders'
    # Nossos apps
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zapsign_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {

            'context_processors': [
                # default context processors—ensure these are present
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },

]

WSGI_APPLICATION = 'zapsign_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# ... (configurações de senha e internacionalização)

# Configs da API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ZapSign Challenge API',
    'DESCRIPTION': 'API para o desafio técnico da ZapSign.',
    'VERSION': '1.0.0',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

STATIC_URL = 'static/'

CORS_ORIGIN_ALLOW_ALL = True