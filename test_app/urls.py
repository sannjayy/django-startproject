from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import send_test_email_view, SuperPanelActionsView

app_name = 'test'

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='app_test/home.html')), name='home'),
    path('email/', send_test_email_view, name='email'),
    path('quick/actions', SuperPanelActionsView, name='spanel'),
]