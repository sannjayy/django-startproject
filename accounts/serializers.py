from dataclasses import field
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import SocialLogin, UserProfile, SOCIAL_LOGIN_PROVIDERS
from .emails import AccountEmail

# LOGIN SERIALIZER
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, min_length=1)
    class Meta:
        model = User
        fields=['username', 'password', 'device_info']
        

# SOCIAL LOGIN SERIALIZER 
class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=SOCIAL_LOGIN_PROVIDERS, write_only=True, error_messages={'required': 'provider is required.'})
    social_token = serializers.CharField(max_length=255, write_only=True, error_messages={'required': 'unique social token is required.'})
    full_name = serializers.CharField(max_length=255, write_only=True, error_messages={'required': 'full name is required.'})
    email = serializers.EmailField(write_only=True, allow_null=True, error_messages={'required': 'email is required.'}, required=False)
    device_info = serializers.JSONField(default=dict, required=False, allow_null=True, write_only=True)
  

    class Meta:
        fields=['provider', 'social_token', 'full_name', 'email', 'device_info']
        extra_kwargs = {
            "full_name": { 'required': True, "error_messages": {"required": "Full name is required."}},
        }
        error_messages = {"social_token": {"required": "unique social token is required."}}


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'is_primary', 'is_kid')


#  Social Account Serializer
class SocialLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLogin
        fields = ('id', 'provider')


# AUTH SERIALIZER (Registration, Login, Social Login)
class AuthenticationSerializer(serializers.ModelSerializer):
    linked_accounts = SocialLoginSerializer(read_only=True, many=True)
    profiles = UserProfileSerializer(read_only=True, many=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'account_name', 'username', 'mobile', 'is_mobile_verified', 'email', 'is_email_verified', 'gender',  'referral_id', 'date_of_birth', 'is_active', 'created_at', 'updated_at', 'last_login', 'profiles', 'linked_accounts', 'tokens')

    def get_tokens(self, obj):
        user = User.objects.get(username = obj.username)
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh'],
        }
    

# USER ACCOUNT SERIALIZER
class UserAccountSerializer(serializers.ModelSerializer):
    linked_accounts = SocialLoginSerializer(read_only=True, many=True)
    profiles = UserProfileSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'account_name', 'username', 'mobile', 'is_mobile_verified', 'email', 'is_email_verified', 'gender',  'referral_id', 'date_of_birth', 'is_active', 'created_at', 'updated_at', 'last_login', 'profiles', 'linked_accounts')


# USER REGISTER SERIALIZER
class RegisterSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(default='male')
    mobile = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'mobile', 'referral_code', 'gender', 'device_info', 'password', )
        
        extra_kwargs = {
            "password": {'write_only': True},
            "device_info": {'write_only': True},
        }    

    def create(self, validated_data):
        email = validated_data.get('email', None)
        mobile = validated_data.get('mobile', None)
        referral_code = validated_data.get('referral_code', None)
        device_info = validated_data.get('device_info', None)


        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            email=email,
            mobile=mobile,
            gender=validated_data['gender'],
            referral_code=referral_code,
            device_info=device_info or None,
            username=None,
            password=validated_data['password'],
        )
        SocialLogin.objects.create(
            user = user,
            token = email,
            provider = 'email'
        )

        # Send Email
        if email:
            AccountEmail().send_email_verification_email(user)        

        return user    

  
# LOGOUT SERIALIZER
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            raise serializers.ValidationError('Token is expired or invalid') from e


# Password Change Serializer
class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password', False)
        password = attrs.get('password', False)
        password2 = attrs.get('password2', False)

        if not old_password or not password or not password2:
            raise serializers.ValidationError("fields 'old_password', 'password', 'password2' is required.")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is not correct.")

        if password != password2:
            raise serializers.ValidationError("Password fields didn't match.")

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        # Send Password Change Email
        if instance.email:
            AccountEmail().send_account_password_changed_email(instance)         
        
        return instance


# Account Update Serializer
class AccountUpdateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'username', 'email', 'is_email_verified')
        read_only_fields = ('is_email_verified', 'is_mobile_verified',)
   

    def update(self, instance, validated_data):
        # If email changed Make email unverified
        if validated_data.get('email'):
            email = validated_data.get('email')
            if instance.email != email:
                instance.is_email_verified = False
                instance.save()
                # Send email notification
                AccountEmail().email_changed_verification_email(instance)            
        
        return super().update(instance, validated_data)


# User Email Verification Serializer
class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User
        fields = ['token']


# Mobile Serializer
class MobileSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)
    class Meta:
        fields = ['mobile']


# Mobile + OTP Serializer
class MobileOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)


# Email + OTP Serializer
class EmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    class Meta:
        model = User
        fields = ['email', 'otp']


# User Password Reset via OTP Serializer
class ResetPasswordOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(min_length=4, max_length=68)

    class Meta:
        fields=['mobile', 'otp', 'password']