import os

# Site Information
COMPANY_NAME = os.environ.get("COMPANY_NAME") # Znas Solutions Pvt. Ltd
PROJECT_TITLE = os.environ.get("PROJECT_TITLE") # Znas OTT Platform
PROJECT_SHORT_TITLE = os.environ.get("PROJECT_SHORT_TITLE") # ZnasOTT
PUBLIC_DOMAIN = os.environ.get('PUBLIC_DOMAIN')

# Support Information
SUPPORT_EMAIL = os.environ.get('SUPPORT_EMAIL')
SUPPORT_PHONE = os.environ.get('SUPPORT_PHONE')

# Admin Information
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'me@sanjaysikdar.dev')
CURRENT_VERSION = os.environ.get('CURRENT_VERSION')


# TEXT TEMPLATES
TEXT_TEMPLATES = {
    # ADMIN PANEL
    'django_admin_panel': {
        'header': '{} Admin',
        'title': '{} Admin Portal',
        'index_title': 'Welcome to {} Management',
    },
    # EMAIL DEFAULTS
    'email': {
        'email_footer_text': '{COMPANY_NAME} © {CURRENT_YEAR}. All Rights Reserved.',
    }
}
