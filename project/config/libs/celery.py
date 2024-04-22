import os



# Celery settings
REDIS_HOST_URL = f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT', '6379')}/0"
CELERY_TIMEZONE = os.environ.get('TIME_ZONE', 'Asia/Kolkata')
CELERY_BROKER_URL = REDIS_HOST_URL
CELERY_RESULT_BACKEND = REDIS_HOST_URL

# CELERY_CACHE_BACKEND = 'default'
CELERY_BROKER_HEARTBEAT = 10
CELERY_BROKER_POOL_LIMIT = 10
CELERY_BROKER_CONNECTION_TIMEOUT = 60
CELERY_TASK_PUBLISH_RETRY = True
CELERY_TASK_RESULT_EXPIRES = 86400


CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_EXTENDED = True
CELERY_TASK_DEFAULT_PRIORITY = 3

CELERY_ALWAYS_EAGER=True
# Celery Configuration Options
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_TASK_TRACK_STARTED = True
CELERY_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 60 * 60  # 3600 seconds (60 minutes)
CELERY_BROKER_HEARTBEAT_TIMEOUT = 30
BROKER_CONNECTION_OPTION = True
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
# CELERYD_MAX_TASKS_PER_CHILD = 1000

# CELERY_IMPORTS = ('test_app.tasks',)  # Import path to your Celery tasks module

if (os.environ.get('ENABLE_CELERY_BEAT') == 'True'):
    from celery.schedules import crontab
    
    CELERY_RESULT_BACKEND = 'django-db'
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    # CELERY_BEAT_SCHEDULE = {
        
    #     'every-10-seconds': {
    #         'task': 'app_mongo.tasks.clear_session_cache',
    #         'schedule': crontab(minute='*/1'),
    #         'args': ('111', )
    #     }
    # }
