from project.settings.config import OTP_SMS_TEMPLATE
from rest_framework.response import Response
from rest_framework import status, generics, views
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import jwt 
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from utils import generate_random_password
from utils.sms import SMSUtil
from .permissions import IsUser
from .utils import HandleUserCount
from .models import SocialLogin
from .emails import AccountEmail
from .serializers import LoginSerializer, RegisterSerializer,  UserAccountSerializer, LogoutSerializer, AccountUpdateSerializer, PasswordChangeSerializer, VerifyEmailSerializer, SocialAuthSerializer, MobileSerializer, MobileOTPSerializer, ResetPasswordOTPSerializer, EmailOTPSerializer
User = get_user_model()

# USER ACCOUNT VIEW
class UserAccountView(generics.GenericAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = (IsAuthenticated, IsUser)

    @swagger_auto_schema(tags=['Account Management'])
    def get(self, request):
        """ 
            Returns Current Authenticated User's Info
        """
        serializer = self.serializer_class(request.user)
        return Response({'success': True, 'detail': 'success.', 'data': serializer.data}, status=status.HTTP_200_OK)
    

# USERNAME & PASSWORD AUTHENTICATION VIEW
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [AnonRateThrottle]
    @swagger_auto_schema(tags=['Account Management'])
    def post(self, request):
        """Login With Username and Password"""
        serializer = self.serializer_class(data = request.data)

        if not serializer.is_valid(raise_exception=False):
            errors_list = [f"{key}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response( {'success': True, 'detail': 'Login success.', 'data':serializer.data}, status=status.HTTP_200_OK)


# SOCIAL AUTHENTICATION / REGISTRATION VIEW
class SocialLogicAPIView(generics.GenericAPIView):
    serializer_class = SocialAuthSerializer
    user_serializer = LoginSerializer

    @swagger_auto_schema(tags=['Account Management'])
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
    

# USER REGISTRATION (PASSWORD) VIEW
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer  

    @swagger_auto_schema(tags=['Account Management'])
    def post(self, request):
        """Account Registration with Email and Password"""
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


# LOGOUT SINGLE DEVICE
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=['Account Management'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)


# LOGOUT ALL DEVICES
class LogoutAllAPIView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(tags=['Account Management'])
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


# Account Update API View
class AccountUpdateAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsUser)
    serializer_class = AccountUpdateSerializer
    throttle_classes = [UserRateThrottle]
    
    @swagger_auto_schema(tags=['Account Management'])
    def patch(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid(raise_exception=False):
            errors_list = [f"{key}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.save()
        return Response({'success': True, 'detail': 'Account has been updated.'}, status=status.HTTP_200_OK)


# Password Change API View
class PasswordChangeAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, IsUser)
    serializer_class = PasswordChangeSerializer
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(tags=['Account Management'])
    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid(raise_exception=False):
            errors_list = [f"{key}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
        
        instance.set_password(serializer.validated_data['password'])
        instance.save()
            
        # Send Password Change Email
        if instance.email:
            AccountEmail().send_account_password_changed_email(instance)  
        return Response({'success': True, 'detail': 'Password has been changed.'}, status=status.HTTP_200_OK)
       

# Resend Email Verification Mail
class ResendVerifyEmailAPIView(views.APIView):
    permission_classes = (IsAuthenticated, IsUser)
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(tags=['Account Management'])
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


# Verify Email (Token) Address API View
class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    throttle_classes = [AnonRateThrottle]

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Verification token", type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config], operation_description="Verify e-mail address", tags=['Account Management'])
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


# Verify Email via OTP API View [OTP]
class VerifyEmailOTPAPIView(generics.GenericAPIView):
    serializer_class = EmailOTPSerializer
    throttle_classes = [AnonRateThrottle]

    @swagger_auto_schema(tags=['Account Management'])
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


# Send OTP SMS 
class SendOTPSMSAPIView(generics.GenericAPIView):
    """Send OTP SMS"""
    serializer_class = MobileSerializer
    throttle_classes = [AnonRateThrottle]

    @swagger_auto_schema(tags=['Account Management'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):           
            errors_list = [f"{key}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)
        # mob=''
        mobile = serializer.data.get('mobile')
        # mob = mobile
        # if '+91' not in mobile:
        #     mob = f"+91{mobile}"

        # print(mob)
        user = ''
        user = User.objects.filter(mobile=mobile).first()
        if '+91' not in mobile and not user:
            user = User.objects.filter(mobile=f"+91{mobile}").first()
        if not user:
            return Response({'success': False,'detail': 'Please contact customer care.'}, status=status.HTTP_404_NOT_FOUND)        

        if not user.is_active:
            return Response({'success': False,'detail': 'Account not activated. Please contact customer care.'}, status=status.HTTP_404_NOT_FOUND)        

        count_response = HandleUserCount(user).has_sms_verification_sent_limit()
        if count_response['has_error']:
            return Response({'success': False, 'detail': count_response['detail']}, status=status.HTTP_400_BAD_REQUEST)

        user.otp.regenerate()
        
        msg = OTP_SMS_TEMPLATE.format(
            username=user.username,
            otp=user.otp.code
        ) # Prepare Template
        SMSUtil.send_sms(mobile=mobile, msg=msg) # <- Send OTP
        # AccountEmail().send_email_otp_mail(user) # <- Send Email

        return Response({'success': True, 'detail': f'We have sent a OTP ({user.otp.code}) to your mobile number. ', 'mobile': mobile}, status=status.HTTP_200_OK)


# Reset Password via OTP API View [OTP] (Step 2)
class PasswordOTPResetAPIView(generics.GenericAPIView):
    """Password Reset Using OTP (Step 2)"""
    serializer_class = ResetPasswordOTPSerializer
    permission_classes = (IsUser,)

    @swagger_auto_schema(tags=['Account Management'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=False):           
            errors_list = [f"{key}: {value[0]}" for key, value in serializer.errors.items()]
            return Response({'success': False, 'detail': errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)        
      
        mobile = serializer.data.get('mobile')
        user_otp = serializer.data.get('otp')
        password = serializer.data.get('password')
        user = ''
        user = User.objects.filter(mobile=mobile).first()
        if '+91' not in mobile and not user:
            user = get_object_or_404(User, mobile=f"+91{mobile}")
        if user.otp.code == user_otp:
            user.set_password(password)
            user.save()

            user.otp.regenerate()
            # Send Reset Password Email
            AccountEmail().send_account_password_changed_email(user)
            return Response({'success': True, 'detail': "Password set successfully."}, status=status.HTTP_200_OK)

        return Response({'success': False, 'detail': "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


