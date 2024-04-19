from django.shortcuts import render, redirect
from django.views import generic
from utils.email import EmailUtil
from .forms import EmailForm, ActionsListForm
from utils.functions import dotdict
from project.config import EMAIL_CONSTANTS, ADMIN_EMAIL
from random import randint
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

import os
# Create your views here.



class TestHomePageView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name="app_test/home.html"
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class TestConfigDetailPage(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = "app_test/config_view.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context

   
    
class TestSystemInfoView(generic.TemplateView):
    template_name="app_test/system.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        

       
        # context['testimonials'] = Testimonial.objects.filter(status=True).order_by('order')

        return context










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
                **EMAIL_CONSTANTS
            }, template_name='app_test/emails/test_mail_template.html')
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
            from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
            tokens = BlacklistedToken.objects.all()
            for token in tokens:
                token.delete()
            messages.success(request, 'Deleted All Blacklisted Tokens.')

        elif action == 'OutstandingToken':
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
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




@login_required(login_url='/admin/login/')
def test_celery_view(request):
    from test_app.models import CeleryTest
    # celery_test_func.delay('sanjay')
    if os.environ.get('ENABLE_CELERY') == 'True':
        from test_app.task import celery_test_func

        if request.method == 'POST':
            celery_test_func.apply_async(args=[f'test_{randint(1, 99)}'])
            messages.success(request, 'Action triggered try refreshing the page.')
            return  redirect(request.META.get('HTTP_REFERER'))
        tasks = CeleryTest.objects.all()
        return render(request, 'app_test/celery.html', context={'tasks': tasks})
    # return  redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/admin/login/')
def delete_celery_tasks(request):
    from test_app.models import CeleryTest
    CeleryTest.objects.all().delete()
    messages.success(request, 'All task has been deleted.')
    return redirect(request.META.get('HTTP_REFERER'))