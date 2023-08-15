from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
User = get_user_model()


# Email or Username Login
class EmailORUsernameLoginBackend(ModelBackend):
    ''' Login with Email or Username Implemented '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: 
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            
        except UserModel.DoesNotExist:
            UserModel().set_password(password)

        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)

        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None