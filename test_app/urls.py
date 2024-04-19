from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import TestConfigDetailPage, TestHomePageView, TestSystemInfoView, send_test_email_view, SuperPanelActionsView

app_name = 'test'

urlpatterns = [
    path('', TestHomePageView.as_view(), name='home'),
    path('<slug>/', TestConfigDetailPage.as_view(), name='config_detail'),
    path('', TestSystemInfoView.as_view(), name='system_info'),
    path('email/', send_test_email_view, name='email'),
    path('quick/actions', SuperPanelActionsView, name='spanel'),
]