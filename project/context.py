
from project.config import ENABLE_SWAGGER
import os
from utils.boto3 import get_domain

def global_context(request):
    # Define the keys for which you want to retrieve values
    keys = [
        "DEBUG_VALUE", "ENV_NAME", "ENABLE_LOGGER", "COMPANY_NAME", "PROJECT_TITLE", "PROJECT_SHORT_TITLE", "USE_ADMIN_LOGO",
        "SUPPORT_EMAIL", "SECRET_KEY", "ALLOWED_HOSTS", "CORS_ALLOWED_ORIGINS", "PUBLIC_DOMAIN",
        "CURRENT_VERSION", "ADMIN_EMAIL", "TIME_ZONE", "LANGUAGE_CODE", "ENABLE_TEST_PANEL", "ENABLE_SYSINFO", "ENABLE_DRF",
        "ENABLE_SWAGGER", "USE_ASGI_MODE", "ENABLE_CRON_JOBS", "ENABLE_CELERY", "ENABLE_CELERY_BEAT", "ENABLE_SMTP", "EMAIL_HOST",
        "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD", "EMAIL_PORT", "EMAIL_USE_TLS", "DEFAULT_FROM_EMAIL",
        "ENABLE_SMS_GATEWAY", "SMS_GATEWAY_HOST", "SMS_GATEWAY_API_KEY", "SMS_GATEWAY_SENDER_ID", "ENABLE_DB",
        "DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_TYPE", "ENABLE_MONGO_ENGINE",
        "MONGODB_CONNECTION_STRING", "ENABLE_REDIS", "REDIS_CHANNEL_LAYER", "REDIS_HOST", "REDIS_PORT",
        "ENABLE_AWS_S3_STORAGE", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_S3_STORAGE_BUCKET_NAME",
        "AWS_S3_REGION_NAME", "AWS_S3_CUSTOM_DOMAIN", "DEFAULT_FILE_UPLOAD_DIR"
    ]

    # Initialize a dictionary to store key-value pairs
    values = {}

    # Retrieve values for each key
    for key in keys:
        values[key] = os.environ.get(key)

    values['AWS_S3_CUSTOM_DOMAIN'] = get_domain()
    return {
        'env': values
    }