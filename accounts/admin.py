from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission, Group
from import_export.admin import ImportExportModelAdmin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin, BlacklistedTokenAdmin

from .models import Otp, User, SocialLogin, UserCoordinate, UserProfile
from .forms import UserChangeForm, UserCreationForm
from .resources import UsersResource

# Users Social Login  
class SocialLoginInline(admin.StackedInline):
    model = SocialLogin
    autocomplete_fields = ["user"]
    readonly_fields=('provider', 'token',)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return None

# Users Profiles    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    readonly_fields=('is_primary', 'is_kid', 'status',)
    
# User Coordinate Inline
class UserCoordinateInline(admin.StackedInline):
    model = UserCoordinate
    readonly_fields=('latitude', 'longitude',)
    extra = 0
    
    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)

# Users OTP
class UserOTPInline(admin.StackedInline):
    model = Otp
    readonly_fields=('code', 'count',)
    extra = 0
    
    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)


# Primary User Admin
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # List admin
    resource_class = UsersResource
    inlines = (UserProfileInline, UserOTPInline, UserCoordinateInline, SocialLoginInline)
    list_display = ('full_name', 'email', 'referral_id', 'created_at', 'updated_at',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    readonly_fields = ('referral_code', 'gender', 'date_of_birth', 'device_info')
    list_display_links = ('full_name', 'email')
    fieldsets = (
        ('Account Information', {'fields': ('full_name', 'gender', 'date_of_birth', 'referral_code', 'device_info')}),
        ('User Credentials', {'fields': ('email', 'is_email_verified', 'mobile', 'is_mobile_verified','username', 'password',)}),
        
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}), # 'user_permissions', 'groups'
    )
    # Creating new user from admin
    add_fieldsets = (
        ('User Information', {'classes': ('wide',), 'fields': ('full_name', 'email', 'mobile', 'password1', 'password2',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        
    )
    search_fields = ('email', 'mobile', 'full_name', 'username')
    ordering = ('-created_at',)
    filter_horizontal = ('groups',)
    list_per_page = 17

# User Admin Register
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
# admin.site.register(Permission)


# admin.site.unregister(Permission)


# Token Blacklist 
# class OutstandingTokenAdmin(token_blacklist.admin.BlacklistedTokenAdmin):

class OutstandingTokenAdmin(OutstandingTokenAdmin):
    ordering = OutstandingTokenAdmin.ordering = ("-created_at",) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        ordering = ("-created_at",)
    def has_delete_permission(self, *args, **kwargs):
        return False # or whatever logic you want