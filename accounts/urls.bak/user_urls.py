from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from ..views.user_views import LoginAPIView, RegisterAPIView, UserAccountView, LogoutAPIView, LogoutAllAPIView, AccountUpdateAPIView, PasswordChangeAPIView, ResendVerifyEmailAPIView, VerifyEmailAPIView, PasswordResetEmailAPIView, PasswordResetTokenVerifyAPIView, ResetPasswordAPIView, VerifyEmailOTPAPIView, VerifyEmailOTPResendAPIView, UserReferralListAPIView, SocialLogicAPIView, UserCoordinateUpdateAPIView


urlpatterns = [
    path('user', UserAccountView.as_view(), name="account"),    
    path('user/login', LoginAPIView.as_view(), name='login'),
    path('user/login/social', SocialLogicAPIView.as_view(), name='social_login'),

    path('user/coordinate/update', UserCoordinateUpdateAPIView.as_view(), name='coordinates_update'),

    # path('admin/login', AdminLoginAPIView.as_view(), name='admin_login'),
    path('user/register', RegisterAPIView.as_view(), name='register'),
    path('user/token/verify', TokenVerifyView.as_view(), name="verify_token"),
    path('user/token/refresh', TokenRefreshView.as_view(), name="refresh_token"),
    path('user/logout', LogoutAPIView.as_view(), name='logout'),
    path('user/logout/all', LogoutAllAPIView.as_view(), name='logout_all'),
    path('user/update/<pk>', AccountUpdateAPIView.as_view(), name="account_update"),     
    path('user/password/change/<pk>', PasswordChangeAPIView.as_view(), name="password_change"), 

    # path('user/referrals', UserReferralListAPIView.as_view(), name="user_referral_list"),   

    # Forgot Password
    path('user/password/forgot', PasswordResetEmailAPIView.as_view(), name="forgot_password"),
    path('user/password/verify/<uidb64>/<token>', PasswordResetTokenVerifyAPIView.as_view(), name="forgot_password_token_verify"),  
    path('user/password/reset', ResetPasswordAPIView.as_view(), name="reset_password"),  

    # Account Email Verification
    path('verify/email', VerifyEmailAPIView.as_view(), name="verify_email"),   
    path('verify/email/resend', ResendVerifyEmailAPIView.as_view(), name="resend_verify_email"), 
    # path('verify/otp/email', VerifyEmailOTPAPIView.as_view(), name="verify_otp_email"),   
    # path('verify/otp/email/resend', VerifyEmailOTPResendAPIView.as_view(), name="resend_email_otp"), 
]