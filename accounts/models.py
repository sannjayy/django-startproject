from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group, AbstractBaseUser, PermissionsMixin
from django.utils.crypto import get_random_string
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.text import slugify

from accounts.options import GENDER_OPTIONS
from .utils import random_code_generator
from .manager import UserManager
import os


# Extend Django Auth Group 
class Group(Group):
    class Meta:
        proxy = True
        verbose_name_plural = 'User Groups'

# Primary User Model
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    
    # Primary Fields
    full_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, null=True, validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    mobile = PhoneNumberField(null=True, blank=True, help_text="Mobile Number should start with +91 followed by 10 digits.")
    is_mobile_verified = models.BooleanField(default=False)    

    # Counts
    counts =  models.JSONField(default=dict, null=True, blank=True)
    referral_id = models.CharField(max_length=50, null=True, blank=True, editable=False)
    referral_code = models.CharField(max_length=50, null=True, blank=True, help_text="Registration time used referral code.")
    
    # Information
    gender = models.CharField(choices=GENDER_OPTIONS, default=None, max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    device_info =  models.JSONField(default=dict, null=True, blank=True)

    # Permissions
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.")
    is_active = models.BooleanField(default=True, help_text="Unselect this instead of deleting accounts.")
    is_deleted = models.BooleanField(default=False, help_text="Soft Delete User Account.")

    # Date Time
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["password"]

    class Meta:
        verbose_name = 'User Account'   
        ordering = ['-id']    
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username'),
            models.UniqueConstraint(fields=['email'], name='unique_email'),
            models.UniqueConstraint(fields=['mobile'], name='unique_mobile'),
            models.UniqueConstraint(fields=['referral_id'], name='unique_referral_id'),
        ]
        indexes = [
            models.Index(fields=['id'], name='id_idx'),
            models.Index(fields=['mobile'], name='mobile_idx'),
            models.Index(fields=['full_name'], name='full_name_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['is_active'], name='is_active_idx'),
            models.Index(fields=['is_staff'], name='is_staff_idx'),
            models.Index(fields=['is_deleted'], name='is_deleted_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.referral_id:
            self.referral_id = random_code_generator(8)

        if not self.username:  
            username = self.email.split('@')[0] if self.email else slugify(self.full_name[:6]).replace('-','_')
            counter = 1
            while User.objects.filter(username=username):
                username = username + str(counter)
                counter += 1
            self.username = username
        super().save(*args, **kwargs)
    
    def tokens(self):
        if os.environ.get('ENABLE_DRF', 'False').lower() == 'true':
            # If DRF Enabled, return JWT Tokens
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(self)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        return None

    @property
    def account_name(self):
        return self.full_name.title() or self.username.title()
    
    @property
    def nickname(self):
        name = self.full_name or self.username
        return name.split(' ')[0].title()    
    

# USER OTP MODEL
class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, validators=[MinLengthValidator(6)], blank=True)
    count = models.PositiveIntegerField(blank=True, null=True, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(6, allowed_chars="0123456789")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User OTP'

    def regenerate(self):
        self.code = get_random_string(6, allowed_chars="0123456789")
        self.save()



SOCIAL_LOGIN_PROVIDERS = (
    ('email', 'email'),
    ('facebook', 'facebook'),
    ('google', 'google'),
    ('apple', 'apple'),
)

class SocialLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='linked_accounts')
    provider = models.CharField(choices=SOCIAL_LOGIN_PROVIDERS, max_length=20, default='google')
    token = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'provider', 'token'], name='unique_social_login'),
        ]
    
    def __str__(self) -> str:
        return self.provider


# User Profile
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=50)
    is_primary = models.BooleanField(default=False)
    is_kid = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} - {self.name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_profile'),
        ]

