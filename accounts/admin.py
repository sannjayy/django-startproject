from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup
from core.utils import import_export_formats
from import_export.admin import ImportExportModelAdmin
from .models import Group, User, UserProfile, Otp, SocialLogin
from .forms import UserChangeForm, UserCreationForm
from .resources import UsersResource
import os

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
  

# Users OTP
class UserOTPInline(admin.StackedInline):
    model = Otp
    readonly_fields=('code', 'count',)
    extra = 0
    
    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)


# Primary User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # List admin
    resource_class = UsersResource
    inlines = (UserProfileInline, UserOTPInline, SocialLoginInline)
    list_display = ('id', 'username', 'full_name', 'email', 'mobile', 'created_at', 'updated_at',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_deleted')
    readonly_fields = ('gender', 'date_of_birth', 'device_info', 'counts')
    list_display_links = ('full_name', 'id', 'username')
    fieldsets = (
        ('Account Information', {'fields': ('full_name', 'gender', 'date_of_birth', 'device_info', 'counts')}),
        ('User Credentials', {'fields': ('email', 'is_email_verified', 'mobile', 'is_mobile_verified','username', 'password',)}),
        
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}), # 'user_permissions', 'groups'
    )
    # Creating new user from admin
    add_fieldsets = (
        ('User Information', {'classes': ('wide',), 'fields': ('full_name', 'email', 'mobile', 'password1', 'password2',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        
    )
    search_fields = ('email', 'mobile', 'full_name', 'username')
    ordering = ('-created_at',)
    filter_horizontal = ('groups',)
    list_per_page = 17

    def has_view_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def has_add_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def has_update_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def get_export_formats(self):
        return import_export_formats()


# GROUPS
admin.site.unregister(BaseGroup) 

@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ('id','name', 'permissions_count')
    ordering = ('id',)
    list_display_links = ( 'name', 'id',)
    list_per_page = 30 
    filter_vertical = ('permissions',)

    def has_view_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def has_add_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def has_update_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)
    def get_export_formats(self):
        return import_export_formats()
    
    def permissions_count(self, obj):
        # return obj.permissions.count()
        return len(obj.permissions.all())
    permissions_count.short_description = 'Total Permissions'



# Token Blacklist 
# class OutstandingTokenAdmin(token_blacklist.admin.BlacklistedTokenAdmin):
if os.environ.get('ENABLE_DRF', 'False').lower() == 'true':
    
    from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin, BlacklistedTokenAdmin
    class OutstandingTokenAdmin(OutstandingTokenAdmin):
        ordering = OutstandingTokenAdmin.ordering = ("-created_at",) 
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
            ordering = ("-created_at",)

        def has_delete_permission(self, *args, **kwargs):
            return bool(self.request.user.is_superuser) # or whatever logic you want