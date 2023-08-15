
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group
from .models import Otp, User, UserCoordinate
from .utils import HandleUserCount

@receiver(post_save, sender=User)
def add_default_group(sender, instance, created, **kwargs):
    if not created:
        return 


    # Creating blank count object for otp re-send
    HandleUserCount(instance).reset()

    # Create a Record for User OTP
    Otp.objects.create(user=instance)       
    UserCoordinate.objects.create(user=instance)           

    # Add Registered Users in Group
    if instance.is_superuser and instance.is_staff:
        group, create = Group.objects.get_or_create(name='Super Admin')
        
    if instance.is_staff and not instance.is_superuser:
        group, create = Group.objects.get_or_create(name='Staff')
    
    if not instance.is_staff:
        group, create = Group.objects.get_or_create(name='User')

    instance.groups.add(group)
    instance.save() 