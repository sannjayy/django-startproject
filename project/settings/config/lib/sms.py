import os

ENABLE_SMS_GATEWAY = (os.environ.get('ENABLE_SMS_GATEWAY') == 'True')
SMS_GATEWAY_HOST = os.environ.get('SMS_GATEWAY_HOST')
SMS_GATEWAY_API_KEY = os.environ.get('SMS_GATEWAY_API_KEY')
SMS_GATEWAY_SENDER_ID = os.environ.get('SMS_GATEWAY_SENDER_ID')