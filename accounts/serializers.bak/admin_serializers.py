from rest_framework import serializers

from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model
User = get_user_model()

# ADMIN LOGIN SERIALIZER
class AdminLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, min_length=1)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username = obj['username'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }
    class Meta:
        model = User
        fields=['id', 'account_name', 'username', 'email', 'is_email_verified',  'password', 'tokens',]
        read_only_fields = ('account_name', 'email', 'is_email_verified')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, please contact admin.')

        if not user.is_staff:
            raise AuthenticationFailed('You do not have permission to access admin.')

        return {
            'id': user.id,
            'account_name': user.account_name,
            'email': user.email,
            'is_email_verified': user.is_email_verified,
            'username': user.username,
            'tokens': user.tokens,
        }