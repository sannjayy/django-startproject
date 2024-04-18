import os

# REDIS 
ENABLE_REDIS = (os.environ.get('ENABLE_REDIS') == 'True')
if ENABLE_REDIS:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.environ.get('REDIS_HOST'), int(os.environ.get('REDIS_PORT', 6379)))],
            },
        },
    }