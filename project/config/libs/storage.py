import os

ENABLE_AWS_S3_STORAGE = (os.environ.get('ENABLE_AWS_S3_STORAGE') == 'True')
DEFAULT_FILE_UPLOAD_DIR = os.environ.get('DEFAULT_FILE_UPLOAD_DIR', '') # Blank means direct to the media folder, Path Always End with Back Slash

if ENABLE_AWS_S3_STORAGE:
    # AMAZON S3 CONFIG
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') 
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_STORAGE_BUCKET_NAME')
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-south-1')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERIFY = True
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
    DEFAULT_FILE_STORAGE = 'project.storages.MediaStorage'
    STATICFILES_STORAGE = 'project.storages.StaticStorage'
    SECURE_REFERRER_POLICY = 'same-origin'

    # S3 Storage Configurations
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_LOCATION = "static"
    S3_URL = "https://%s" % AWS_S3_CUSTOM_DOMAIN
    
    # Link expiration time in seconds
    AWS_QUERYSTRING_EXPIRE = "3600"
    # REF: https://theyashshahs.medium.com/aws-s3-signed-urls-in-django-d9e66853a42f
    # GOOD REF: https://medium.com/@ekeydar/signed-urls-storage-for-django-58feecbd94a8