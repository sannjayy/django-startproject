from django.urls import path
from accounts.views import LoginAPIView, SocialLogicAPIView, UserAccountView, RegisterAPIView, LogoutAPIView, LogoutAllAPIView, PasswordChangeAPIView, AccountUpdateAPIView, ResendVerifyEmailAPIView, VerifyEmailAPIView, SendOTPSMSAPIView, PasswordOTPResetAPIView, VerifyEmailOTPAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# /v1/{path}
urlpatterns = [
    path('users/registation', RegisterAPIView.as_view(), name='register'),
    path('users/me', UserAccountView.as_view(), name="account"),    
    path('users/login', LoginAPIView.as_view(), name='login'),
    path('users/login/social', SocialLogicAPIView.as_view(), name='social_login'),

    # path('users/token/verify', TokenVerifyView.as_view(), name="verify_token"),
    # path('users/token/refresh', TokenRefreshView.as_view(), name="refresh_token"),

    path('users/logout', LogoutAPIView.as_view(), name='logout'),
    path('users/logout/all', LogoutAllAPIView.as_view(), name='logout_all'),
    path('users/update', AccountUpdateAPIView.as_view(), name="account_update"),    
    path('users/password/change', PasswordChangeAPIView.as_view(), name="password_change"), 

    path('verify/email/token', VerifyEmailAPIView.as_view(), name="verify_email"),   
    path('verify/email/token/resend', ResendVerifyEmailAPIView.as_view(), name="resend_verify_email"), 

    path('send/otp', SendOTPSMSAPIView.as_view(), name="forgot_password_otp_send"), 
    path('password/reset', PasswordOTPResetAPIView.as_view(), name="forgot_password_otp_reset"), 

    path('verify/email/otp', VerifyEmailOTPAPIView.as_view(), name="verify_otp_email"),   
]