import os

# SMTP CONFIG
ENABLE_SMTP = (os.environ.get('ENABLE_SMTP') == 'True')
if ENABLE_SMTP:
    EMAIL_USE_TLS = (os.environ.get('EMAIL_USE_TLS', True) == 'True')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587)) # 587/465
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') # Znas Cloud <info@znascloud.com>
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

