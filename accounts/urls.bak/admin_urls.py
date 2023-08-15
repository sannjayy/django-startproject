from django.urls import path
from ..views.admin_views import AdminLoginAPIView, UsersListView, UserDetailAPIView, AdminUserReferralListAPIView


urlpatterns = [
    path('login', AdminLoginAPIView.as_view(), name='admin_login'),
    path('users', UsersListView.as_view(), name="all_users_list"),
    path('users/<username>', UserDetailAPIView.as_view(), name="user_detail"),
    path('users/referrals/<int:user_id>', AdminUserReferralListAPIView.as_view(), name="user_referrals"),
    
]