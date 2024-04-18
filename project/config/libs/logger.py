
import os
from project.settings.base import BASE_DIR

# LOGGER 
ENABLE_LOGGER = (os.environ.get('ENABLE_LOGGER') == 'True')
if ENABLE_LOGGER:
    APP_LOG_FILENAME = BASE_DIR / 'logs/app.log'
    ERROR_LOG_FILENAME = BASE_DIR / 'logs/app-error.log'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(name)-12s %(levelname)-8s %(message)s',
            },
            'file': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[{server_time}] {message}',
                'style': '{',
            }
        },    
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'formatter': 'file',
                'filename': APP_LOG_FILENAME
            }
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['console', 'file']
            }
        }
    }