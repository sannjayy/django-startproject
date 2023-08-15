from rest_framework.response import Response
# Password Reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import permissions, status, generics, views
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import jwt, datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone  
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

from utils import generate_random_password
from ..permissions import IsUser
from ..utils import HandleUserCount, isBase64
from ..emails import AccountEmail
from ..serializers import LoginSerializer, RegisterSerializer,  UserAccountSerializer, LogoutSerializer, AccountUpdateSerializer, PasswordChangeSerializer, VerifyEmailSerializer, EmailSerializer, ResetPasswordSerializer, VerifyEmailOTPSerializer, MinimalUserDataSerializer, SocialAuthSerializer, UserCoordinateSerializer
from ..models import SocialLogin, UserCoordinate
User = get_user_model()
# from .models import Otp


# USER AUTHENTICATION VIEW
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        # serializer.is_valid(raise_exception=True)

        if not serializer.is_valid():
            errors_list = [error[0] for error in serializer.errors.values()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response( {'success': True, 'detail': 'Login success.', 'data':serializer.data}, status=status.HTTP_200_OK)


# USER REGISTER VIEW
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer  
    
    def post(self, request):
        data = request.data

        if mobile := data.get('mobile'):
            if User.objects.filter(mobile=mobile).exists():
                return Response({'success': False, 'detail': 'User Account with this mobile already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=False):
            errors_list = [error[0] for error in serializer.errors.values()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'success': True, 'detail': 'Registration success.', 'data': serializer.data}, status=status.HTTP_201_CREATED)


# USER ACCOUNT VIEW
class UserAccountView(generics.GenericAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = (IsAuthenticated, IsUser)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response({'success': True, 'detail': 'success.', 'data': serializer.data}, status=status.HTTP_200_OK)


# LOGOUT SINGLE DEVICE
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)


# LOGOUT ALL DEVICES
class LogoutAllAPIView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


# Account Update API View
class AccountUpdateAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    serializer_class = AccountUpdateSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated, IsUser)


# Password Change API View
class PasswordChangeAPIView(generics.UpdateAPIView):
    http_method_names = ['patch']
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated, IsUser)
    serializer_class = PasswordChangeSerializer
    throttle_classes = [UserRateThrottle]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)       
            return Response({'success': True, 'detail': 'Password has been changed.'}, status=status.HTTP_200_OK)
        errors_list = [error[0] for error in serializer.errors.values()]
        return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)

# Resend Verification Email
class ResendVerifyEmailAPIView(views.APIView):
    permission_classes = (IsAuthenticated, IsUser)
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        user = request.user
        if not user.email:
            return Response({'success': False, 'detail': 'Email not updated on account.'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_email_verified:
            return Response({'success': False, 'detail': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        count_response = HandleUserCount(user).has_email_verification_sent_limit()
        if count_response['has_error']:
            return Response({'success': False, 'detail': count_response['detail']}, status=status.HTTP_400_BAD_REQUEST)

        AccountEmail().send_email_verification_email(user) # <- Send Email
        return Response({'success': True, 'detail': 'We have sent you a link to verify your account.'}, status=status.HTTP_200_OK)


# Verify Email Address API View
class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    throttle_classes = [AnonRateThrottle]

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Verification token", type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config], operation_description="Verify e-mail address")
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # print('payload', payload)
            
            user = get_object_or_404(User, id=payload['user_id'])
            if not user.is_email_verified:
                user.is_email_verified = True                              
                user.save()

                # Send Welcome Mail
                AccountEmail().send_email_verified_email(user)
                return Response({'success': True, 'detail': "Successfully verified."}, status=status.HTTP_200_OK)
            return Response({'success': False, 'detail': "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'success': False, 'detail': "Verification link expired."}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'success': False, 'detail': "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# Resend Verification Email
class VerifyEmailOTPResendAPIView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user = get_object_or_404(User, email=email)

        if not user.email:
            return Response({'success': False,'detail': 'Email not updated on account.'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_email_verified:
            return Response({'success': False, 'detail': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        count_response = HandleUserCount(user).has_email_verification_sent_limit()
        if count_response['has_error']:
            return Response({'success': False, 'detail': count_response['detail']}, status=status.HTTP_400_BAD_REQUEST)
        
        user.otp.regenerate()
        AccountEmail().send_email_otp_verification_email(user) # <- Send Email

        return Response({'success': True, 'detail': 'We have sent a new OTP to your e-mail address.'}, status=status.HTTP_200_OK)


# Verify Email OTP API View
class VerifyEmailOTPAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailOTPSerializer
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user_otp = serializer.data.get('otp')
        user = get_object_or_404(User, email=email)
        if user.is_email_verified:
            return Response({'success': False, 'detail': "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)
            
        if user.otp.code == user_otp:
            user.is_email_verified = True
            user.save()
            # Send Welcome Mail
            AccountEmail().send_email_verified_email(user)
            return Response({'success': True, 'detail': "Email successfully verified."}, status=status.HTTP_200_OK)

        return Response({'success': False, 'detail': "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


# Forgot Password (Step 1)
class PasswordResetEmailAPIView(generics.GenericAPIView):
    """Forgot Password (Step 1)"""
    serializer_class = EmailSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        email =  request.data.get('email', '')

        if User.objects.filter(email=email, ).exists():
            user = User.objects.get(email=email)
            # Send Password Reset Email
            AccountEmail().send_forgot_password_email(user)
            return Response({'success': True, 'detail': 'We have sent you a link to reset your password.'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'detail': 'Email is not registered with us.'}, status=status.HTTP_404_NOT_FOUND)


# Verify Password Reset Link Token (Step 2)
class PasswordResetTokenVerifyAPIView(views.APIView):
    """Verify Forgot Password Reset Link Token (Step 2)"""
    def get(self, request, uidb64, token): 
        # sourcery skip: avoid-builtin-shadow
        if not isBase64(uidb64):
            return Response({'success': False, 'detail': 'Invalid uidb64 token provided.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user=get_object_or_404(User, id=id)
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': True, 'detail': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

            return Response({'success': False, 'detail': 'Token is not valid, link has been expired.'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except DjangoUnicodeDecodeError as identifier:
            return Response({'success': False, 'detail': 'Invalid token or link has been expired.'}, status=status.HTTP_401_UNAUTHORIZED)

# 
# Reset Password (Step 3)
class ResetPasswordAPIView(generics.GenericAPIView):
    """Reset Password (Step 3)"""
    serializer_class = ResetPasswordSerializer
    permission_classes = (IsUser,)
    
    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True, 'email': serializer.validated_data.email, 'detail': 'Password reset success.'}, status=status.HTTP_200_OK)
        
        errors_list = [error[0] for error in serializer.errors.values()]
        return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)



# Get User's Referrals
class UserReferralListAPIView(generics.ListAPIView):
    model = User
    serializer_class = MinimalUserDataSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user = request.user
        users = self.model.objects.filter(referral_code=user.referral_id)
        serializer = self.serializer_class(users, many=True)
        if users:
            return Response({'success': True, 'detail': f'Found {users.count()} referrals.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'detail': 'No referral found...'}, status=status.HTTP_404_NOT_FOUND)

        

# SOCIAL LOGIN VIEW
class SocialLogicAPIView(generics.GenericAPIView):
    serializer_class = SocialAuthSerializer

    user_serializer = LoginSerializer
    def post(self, request):
        '''Social Login / Register API View'''
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            return self.get_values_from_serializer(serializer)

        errors_list = [error[0] for error in serializer.errors.values()]
        return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)    

    # Social Login Handle
    def get_values_from_serializer(self, serializer):
        # sourcery skip: low-code-quality
        provider = serializer.validated_data.get('provider')
        social_token = serializer.validated_data.get('social_token')
        full_name = serializer.validated_data.get('full_name')
        device_info = serializer.validated_data.get('device_info')
        detail = ''
        if provider == 'email':
            return Response({'success': False, 'detail': 'Email login is not allowed.'}, status=status.HTTP_400_BAD_REQUEST)   

        if email := serializer.validated_data.get('email'):
            user_obj = User.objects.filter(email=email).first() # If already registered.
            
            # Saving Device info on Login
            if user_obj and device_info: 
                user_obj.device_info = device_info
                user_obj.save()

            detail = 'Logged with social provider.'
            if user_obj and provider not in user_obj.linked_accounts:
                # Linking Social account to Existing Account
                # print('Linked new provider')
                if is_token_exits := SocialLogin.objects.filter(token=social_token).exists():
                    # Check if token used on another account
                    return Response({'success': False, 'detail': 'Token already linked with another account.'}, status=status.HTTP_400_BAD_REQUEST)

                
                # saving token to account
                user_obj.social_login.create(
                    user = user_obj,
                    token = social_token,
                    provider = provider
                )
                detail = 'Linked with new social provider.'

            # 'Email Auth Part'
            if not user_obj:
                # print('Create new user if not registered. ')
                detail = 'New account registered with email.'
                # Create new user with email if not registered.  
                user_obj = User.objects.create_user(
                    full_name=full_name or '',
                    username=None,
                    email=email or None,
                    password='randompasword',
                    is_email_verified=True,
                )
                SocialLogin.objects.create(
                    user = user_obj,
                    token = social_token,
                    provider = provider
                )
                # Send Welcome Mail
                AccountEmail().send_welcome_email(user_obj)


        elif social_obj := SocialLogin.objects.filter(token=social_token).first():
            # print('Login with token')
            detail = 'Loggged in with token.'
            # If no email but token matches
            user_obj = social_obj.user
        else:
            # print('Register with token')
            detail = 'Account registered with token.'
            # Register with token.
            # email = random_string_generator()
            user_obj = User.objects.create_user(
                full_name=full_name or '',
                username=None,
                email=email,
                mobile=None,
                password=generate_random_password(),
                is_email_verified=True,
            )
            SocialLogin.objects.create(
                user = user_obj,
                token = social_token,
                provider = provider
            )            

        # Validation Token and Provider
        if not user_obj.social_login.filter(token=social_token, provider=provider):
            return Response({'success': False, 'detail': 'Token is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        user = {
            'id': user_obj.id,
            'account_name': user_obj.account_name,
            'email': user_obj.email,
            'gender': user_obj.gender,
            'date_of_birth': user_obj.date_of_birth,
            'username': user_obj.username,
            'referral_id': user_obj.referral_id,
            'referral_code': user_obj.referral_code,
            'linked_accounts': user_obj.linked_accounts,
            'created_at': user_obj.created_at,
            'updated_at': user_obj.updated_at,
            'last_login': user_obj.last_login,
            'tokens': user_obj.tokens,
        }
        user_serializer = self.user_serializer(user)
        return Response( {'success': True, 'detail': detail, 'data':user_serializer.data}, status=status.HTTP_200_OK)




# User Coordinate Update
class UserCoordinateUpdateAPIView(generics.GenericAPIView):
    serializer_class = UserCoordinateSerializer
    permission_classes = (IsAuthenticated, IsUser,)

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)

        if not serializer.is_valid(raise_exception=True):
            errors_list = [error[0] for error in serializer.errors.values()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
         
        obj, _ = UserCoordinate.objects.get_or_create(user=request.user)
        if obj:
            obj.latitude = serializer.validated_data.get('latitude')
            obj.longitude = serializer.validated_data.get('longitude')
            obj.save()
        return Response({'success': True, 'detail': 'Coordinates has been updated.', 'data': {'latitude':obj.latitude, 'longitude':obj.longitude }}, status=status.HTTP_200_OK)
        
        
