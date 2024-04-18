import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(find_dotenv())

# PRODUCTION SECRET!
SECRET_KEY = os.getenv('SECRET_KEY').partition("#")[0]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG_VALUE'] == 'True'

ALLOWED_HOSTS = tuple(os.getenv('ALLOWED_HOSTS').partition("#")[0].strip().replace("'",""))

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'django_crontab',
    'corsheaders',
    'rest_framework', 
    'rest_framework_simplejwt.token_blacklist',
    'import_export',
    'drf_yasg',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
]
LOCAL_APPS = [
    'core', 
    'accounts', 
    'test_app',
    
   
]

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
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailORUsernameLoginBackend',
)

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'project.urls'
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

    
