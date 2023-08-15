from import_export import resources
from .models import User

class UsersResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'is_email_verified', 'user_permissions', 'groups', 'last_login', 'is_superuser')
