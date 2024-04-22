import os

if os.environ.get('ENABLE_CELERY') == 'True':
    from .celery import app as celery_app

    __all__ = ("celery_app",)