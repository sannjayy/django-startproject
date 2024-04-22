import time, os
from celery import shared_task



@shared_task()
def celery_test_func(task_name):  
    from .models import CeleryTest
    for i in range(11):
        obj, created = CeleryTest.objects.get_or_create(name=task_name)
        if not created:      
            obj.process = i*10
            obj.is_completed = i == 10
            obj.save()
        time.sleep(1)
    return "Done"
   