import os

ENABLE_TEST_PANEL = os.environ.get('ENABLE_TEST_PANEL', 'False').lower() == 'true'
ENABLE_SWAGGER = os.environ.get('ENABLE_SWAGGER', 'False').lower() == 'true'
AUTH_PASSWORD_VALIDATORS = os.environ.get('AUTH_PASSWORD_VALIDATORS', 'False').lower() == 'true'
ENV_NAME = os.environ.get("ENV_NAME", "dev")


# ACTIVATE WHEN PROJECT IS IN PRODUCTION MODE
if ENV_NAME == 'prod':

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        # { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
        { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
        # { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
        # { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    ]

    # MORE SECURITIES
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_TRUSTED_ORIGINS = [host.strip() for host in os.getenv('CORS_ALLOWED_ORIGINS').split(',')]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    # When in Dev Mode
    AUTH_PASSWORD_VALIDATORS = []