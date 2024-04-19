import os

# REDIS 

ENABLE_REDIS = (os.environ.get('ENABLE_REDIS') == 'True')
REDIS_CHANNEL_LAYER = (os.environ.get('REDIS_CHANNEL_LAYER') == 'True')
if ENABLE_REDIS:
    if REDIS_CHANNEL_LAYER:
        CHANNEL_LAYERS = {
            "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG": {
                    "hosts": [(os.environ.get('REDIS_HOST'), int(os.environ.get('REDIS_PORT', 6379)))],
                },
            },
        }
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{int(os.environ.get('REDIS_PORT', 6379))}",
        }
    }