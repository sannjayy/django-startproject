from project.settings.base import BASE_DIR, SECRET_KEY
import datetime


# CORS SETTINGS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", # :TODO DELETE
    "http://127.0.0.1:3000", # :TODO DELETE
]

# DJANGO REST FRAMEWORK SETTINGS (Development)
REST_FRAMEWORK = {
    # Common
    "NON_FIELD_ERRORS_KEY" : "detail",

    # Auth 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # Filter
    # "DEFAULT_FILTER_BACKENDS": ['django_filters.rest_framework.DjangoFilterBackend'],
    'SEARCH_PARAM': 'q',

    # Throttle
    "DEFAULT_THROTTLE_RATES": {
        'anon': '50/hour',
        'user': '100/hour',
    }
}

# JWT SETTINGS
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=90),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=45),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer', ),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# MORE SECURITIES
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')