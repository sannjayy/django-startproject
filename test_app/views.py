from unicodedata import category
from django.shortcuts import render
from .forms import EmailForm, ActionsListForm
from utils import EmailUtil, dotdict
from project.settings.config.lib import EMAIL_CONSTANTS
from project.settings.config.main import ADMIN_EMAIL
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
import os
# Create your views here.

@login_required
def send_test_email_view(request):
    form = EmailForm(initial={'email': ADMIN_EMAIL})
    if request.method == 'POST':
        form = EmailForm(request.POST)
        email = request.POST.get('email')
        site_config = dotdict(EMAIL_CONSTANTS.get('site'))
        passowrd_hide_len = 20 if len(settings.EMAIL_HOST_PASSWORD) > 20 else 6 
        EmailUtil.send_mail(
            to=(email,), 
            subject=f'Test Mail from {site_config.title}',
            body_context={
                'message': f'This is a test mail from {get_current_site(request).domain}',
                'smtp': {
                    'is_enabled': settings.ENABLE_SMTP,
                    'host': settings.EMAIL_HOST,
                    'port': settings.EMAIL_PORT,
                    'tls': settings.EMAIL_USE_TLS,
                    'username': settings.EMAIL_HOST_USER,
                    'password': f'####################{settings.EMAIL_HOST_PASSWORD[len(settings.EMAIL_HOST_PASSWORD) - passowrd_hide_len:]}',
                    'from_email': settings.DEFAULT_FROM_EMAIL,
                    'backend': settings.EMAIL_BACKEND,
                },
                'db': {
                    'is_enabled': settings.ENABLE_DB,                    
                    'host': os.environ.get('DB_HOST'),
                    'port': os.environ.get('DB_PORT'),
                    'name': os.environ.get('DB_NAME'),
                    'user': os.environ.get('DB_USER'),
                },
                **EMAIL_CONSTANTS
            },
            template_name='app_test/emails/test_mail_template.html')

        messages.success(request, 'Action triggered check your inbox.')

    return render(request, 'app_test/email.html', context={'form':form})



#  Super Panel Actions View.
@login_required
def SuperPanelActionsView(request): 
    form = ActionsListForm()
    if request.method == 'POST':
        form = ActionsListForm(request.POST)
        action = request.POST.get('action')
        if action == 'BlacklistedToken':
            tokens = BlacklistedToken.objects.all()
            for token in tokens:
                token.delete()
            messages.success(request, 'Deleted All Blacklisted Tokens.')

        elif action == 'OutstandingToken':
            tokens = OutstandingToken.objects.all()
            for token in tokens:
                token.delete()            
            messages.success(request, 'Deleted All Outstanding Tokens.')
        
       
            
        # # MISSING CATEGORY APPS REFETCH
        # elif action == 'resync_missing_app_category':
        #     messages.success(request, 'Resynced Missing App Categories.')

        else:
            messages.error(request, 'Invalid action selected.')

        
        # Send Email Notification
        site_config = dotdict(EMAIL_CONSTANTS.get('site'))
        EmailUtil.send_mail(
            to=(ADMIN_EMAIL,), 
            subject=f'Admin Action Notification from {site_config.title}',
            body_context={
                'message': f'New action has performed by {request.user.nickname}, Action type: {action}',                
                **EMAIL_CONSTANTS
            },
            template_name='app_test/emails/notification_mail_template.html')

    return render(request, 'app_test/spanel.html', context={'form':form})
