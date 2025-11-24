# billing_api/settings.py
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY','secret-key')
DEBUG = os.getenv('DEBUG','True') == 'True'
ALLOWED_HOSTS = ['*']

# --- AÑADIR SIMPLE JWT PARA LA AUTENTICACIÓN ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Paquetes de Terceros
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt', # <-- ¡AGREGADO!
    
    # Aplicaciones Locales
    'users',
    'catalog',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'billing_api.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# --- CONFIGURACIÓN DE BASE DE DATOS NEON (PostgreSQL con SSL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME','neondb'), # Usar el nombre de DB de Neon
        'USER': os.getenv('DB_USER','neondb_owner'), # Usar el usuario de Neon
        'PASSWORD': os.getenv('DB_PASS','npg_tIQgO8UDRco1'), # Usar la contraseña de Neon
        'HOST': os.getenv('DB_HOST','ep-fragrant-leaf-ahnx5wz3-pooler.c-3.us-east-1.aws.neon.tech'), # Usar el host de Neon
        'PORT': os.getenv('DB_PORT','5432'),
        'OPTIONS': {
            'sslmode': 'require', # <-- ¡CRUCIAL para la conexión con Neon!
        }
    }
}

# --- CONFIGURACIÓN JWT (Simple JWT) ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS':(
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10
}

SIMPLE_JWT = {
    # Usar las variables de entorno para los tiempos de vida del token
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_DAYS', 7))),
}

STATIC_URL='static/'
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'