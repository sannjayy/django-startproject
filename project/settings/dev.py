from project.settings.base import BASE_DIR, SECRET_KEY
import datetime


# CORS SETTINGS
CORS_ALLOW_ALL_ORIGINS = True


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
    'EXCEPTION_HANDLER': 'utils.exceptionhandler.custom_exception_handler',

    # Throttle
    "DEFAULT_THROTTLE_RATES": {
        'anon': '500/hour',
        'user': '1000/hour',
    }
}


# JWT SETTINGS
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer', ),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}