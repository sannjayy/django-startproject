from ..main import TEXT_TEMPLATES, PROJECT_TITLE, PUBLIC_DOMAIN, SUPPORT_EMAIL, SUPPORT_PHONE, COMPANY_NAME
from utils import dotdict, CURRENT_YEAR

# EMAIL & SMS CONFIG
SMS_RESEND_ATTEMPT = 50 # How Many Times User Can Resend SMS
SMS_RESEND_TIME = 0 # Gap Between SMS Resend (Minutes)

EMAIL_RESEND_ATTEMPT = 200 # How Many Times User Can Resend Email
EMAIL_RESEND_TIME = 0 # Gap Between Email Resend (Minutes)

# EMAIL PREFERENCES
PASSWORD_CHANGE_EMAIL = True
EMAIL_CHANGE_EMAIL = True
ACCOUNT_UPDATE_EMAIL = True

text = dotdict(TEXT_TEMPLATES.get('email'))

# Email Constant Data
EMAIL_CONSTANTS = {
    'site': {
        'title': PROJECT_TITLE, # Site Title
        'domain': PUBLIC_DOMAIN, # Site Domain
        'email': SUPPORT_EMAIL, # None for blank
        'phone': SUPPORT_PHONE, # None for blank
    },        
	'footer_text': text.email_footer_text.format(COMPANY_NAME=COMPANY_NAME, CURRENT_YEAR=CURRENT_YEAR),
}



