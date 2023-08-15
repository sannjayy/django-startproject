import os

DEFAULT_FILE_UPLOAD_DIR = os.environ.get('DEFAULT_FILE_UPLOAD_DIR')
ENABLE_AWS = (os.environ.get('ENABLE_AWS') == 'True')

if ENABLE_AWS:
    # AMAZON S3 CONFIG
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') 
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERIFY = True
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
    DEFAULT_FILE_STORAGE = 'project.settings.config.storages.MediaStorage'
    STATICFILES_STORAGE = 'project.settings.config.storages.StaticStorage'
    SECURE_REFERRER_POLICY = 'same-origin'