from django.db import models
import os


if os.environ.get('ENABLE_CELERY') == 'True':
    class CeleryTest(models.Model):
        name = models.CharField(max_length=255, unique=True, verbose_name='Task Name')
        process = models.IntegerField(default=0)
        is_completed = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)