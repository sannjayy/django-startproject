import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(find_dotenv(), override=True) # Load Env

# PRIMARY SETUP!
SECRET_KEY = os.environ.get('SECRET_KEY', 'jw+6n5-pxn-b0fuxjtxdn')
DEBUG = os.environ['DEBUG_VALUE'] == 'True'
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS').split(',')]

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# Add 'daphne' to default apps if USE_ASGI_MODE is True
if os.environ['USE_ASGI_MODE'] == 'True':
    DEFAULT_APPS.insert(0, "daphne") 



THIRD_PARTY_APPS = [
    'corsheaders',
    # 'rest_framework', 
    # 'rest_framework_simplejwt.token_blacklist',
    'import_export',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
]
# Add 'django_crontab' to default apps if ENABLE_CRON_JOBS is True
if os.environ['ENABLE_CRON_JOBS'] == 'True':
    THIRD_PARTY_APPS.insert(0, "django_crontab") 

# Add 'rest_framework' to default apps if ENABLE_DRF is True
if os.environ.get('ENABLE_DRF', 'False').lower() == 'true':
    THIRD_PARTY_APPS.insert(2, "rest_framework") 
    THIRD_PARTY_APPS.insert(3, "rest_framework_simplejwt.token_blacklist") 

# Add 'drf_yasg' to default apps if ENABLE_SWAGGER is True
if os.environ.get('ENABLE_SWAGGER', 'False').lower() == 'true':
    THIRD_PARTY_APPS.insert(4, "drf_yasg") 

LOCAL_APPS = [
    'core', 
    'accounts', 
]
# Add 'test_app' to local apps if ENABLE_TEST_PANEL is True
if os.environ['ENABLE_TEST_PANEL'] == 'True':
    LOCAL_APPS.insert(0, "test_app")

# Combine all lists to form INSTALLED_APPS
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
                'project.context.global_context',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailORUsernameLoginBackend',
)

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'project.urls'

if os.environ.get('USE_ASGI_MODE') == 'True':
    ASGI_APPLICATION = 'project.asgi.application'
else: 
    WSGI_APPLICATION = 'project.wsgi.application'

# Internationalization
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Kolkata')
USE_I18N = True
USE_TZ = True
DATETIME_FORMAT = '%Y-%m-%d %H:%i:%s'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / "static/staticfiles"
STATICFILES_DIRS = [ BASE_DIR / 'static']


# URL CONFIG
LOGIN_URL = '/admin/'
LOGOUT_URL = '/admin/logout/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FOR MULTIPLE ACTION ON DJANGO ADMIN
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

# PHONE NUMBER VALIDATION
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = "IN"

if os.environ.get('ENABLE_SWAGGER', 'False').lower() == 'true':
    # SWAGGER SETTINGS
    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Bearer':{
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
            }
        }
    }

    
# IMPORT CONFIG
from ..config import *