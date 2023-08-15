from rest_framework_simplejwt.tokens import RefreshToken
from utils import EmailUtil, dotdict
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from project.settings.config import EMAIL_CONSTANTS, ACCOUNT_UPDATE_EMAIL, PASSWORD_CHANGE_EMAIL, EMAIL_CHANGE_EMAIL, PROJECT_SHORT_TITLE, ACCOUNT_VERIFICATION_SUCCESS_URL, SITE_URL
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone 


class AccountEmail:
    def __init__(self) -> None:
        datetime_now = timezone.localtime(timezone.now())
        self.current_time = datetime_now.strftime("%d-%m-%Y %H:%M:%S")


    def send_email_verification_email(self, user):
        # print('called mail verification email')
        self.send_email_address_verification_mail(user, 'Verification Email', 'Please verify your account.', 'emails/verification_email.html')
    

    def send_email_otp_verification_email(self, user):
        EmailUtil.send_mail(
        to=(user.email,), 
        subject=f'Email Verification OTP - {user.otp.code}',
        body_context={
            'message': f'Dear, {user.nickname} \n Please verify your account with OTP [ {user.otp.code} ].',
            'user': user,
            **EMAIL_CONSTANTS
        },
        template_name='emails/verification_otp_email.html')


    def send_email_verified_email(self, user):
        EmailUtil.send_mail(
        to=(user.email,), 
        subject='Welcome to our Platform',
        body_context={
            'message': 'Welcome to our Platform.',
            'explore_site_url': SITE_URL,
            'user': user,
            **EMAIL_CONSTANTS
        },
        template_name='emails/verification_complete_email.html')
    

    def send_welcome_email(self, user):
        EmailUtil.send_mail(
        to=(user.email,), 
        subject='Welcome to our Platform',
        body_context={
            'message': 'Welcome to our Platform. Thank you for registering with us.',
            'explore_site_url': SITE_URL,
            'user': user,
            **EMAIL_CONSTANTS
        },
        template_name='emails/welcome_email.html')


    def send_account_updated_email(self, user):
        if ACCOUNT_UPDATE_EMAIL:
            EmailUtil.send_mail(
            to=(user.email,), 
            subject='You account updated!',
            body_context={
                'message': f'Dear, {user.nickname} your account account has been updated successfully at {self.current_time}',            
                'user': user,
                **EMAIL_CONSTANTS
            },
            template_name='emails/account_update_email.html')


    def send_account_password_changed_email(self, user):
        if PASSWORD_CHANGE_EMAIL:
            EmailUtil.send_mail(
            to=(user.email,), 
            subject='You password changed successfully.',
            body_context={
                'message': f'Dear, {user.nickname} your account password has been changed successfully at {self.current_time}',            
                'user': user,
                **EMAIL_CONSTANTS
            },
            template_name='emails/account_password_changed_email.html')
    

    def email_changed_verification_email(self, user):
        if EMAIL_CHANGE_EMAIL:
            self.send_email_address_verification_mail(
                user, 
                'Account email address changed verification email', 
                'You have recently changed your email address please verify to continue.', 
                'emails/account_email_change_email.html'
            )


    # Using on `send_email_verification_email` and `email_changed_verification_email`
    def send_email_address_verification_mail(self, user, subject, message, template_name):
        token = RefreshToken.for_user(user).access_token
        verification_url = f'{ACCOUNT_VERIFICATION_SUCCESS_URL}?token={token}'

        EmailUtil.send_mail(to=(user.email,), subject=subject, body_context={'message': message, 'verification_url': verification_url, 'user': user, **EMAIL_CONSTANTS}, template_name=template_name)


    def send_email_otp_mail(self, user):
        EmailUtil.send_mail(
        to=(user.email,), 
        subject=f'Forgot Password OTP - {user.otp.code}',
        body_context={
            'message': f'Dear, {user.nickname} \n We have received your password reset request. Your OTP is  {user.otp.code}. [Do not share with anyone]',
            'user': user,
            **EMAIL_CONSTANTS
        },
        template_name='emails/otp_email.html')


    # def send_forgot_password_email(self, user):

    #     uidb64 = urlsafe_base64_encode(smart_bytes(user.id)) # User ID Encryption
    #     token = PasswordResetTokenGenerator().make_token(user) # Token of User

    #     absolute_url = f'{RESET_PASSWORD_PAGE_URL}?uid={uidb64}&token={token}'
    #     EmailUtil.send_mail(
    #             to=(user.email,), 
    #             subject=f'Forgot Password - {PROJECT_SHORT_TITLE}',
    #             body_context={
    #                 'message': f'Hi, {user.nickname} we have got your password reset request.',            
    #                 'user': user,
    #                 'absolute_url': absolute_url,
    #                 **EMAIL_CONSTANTS
    #             },
    #             template_name='emails/forgot_password_email.html')