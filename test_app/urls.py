from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import os

from .views import TestConfigDetailPage, TestHomePageView, TestSystemInfoView, send_test_email_view, SuperPanelActionsView

app_name = 'test'

urlpatterns = [
    path('', TestHomePageView.as_view(), name='home'),
    # path('', TestSystemInfoView.as_view(), name='system_info'),
    path('test_email/', send_test_email_view, name='email'),
    path('quick/actions', SuperPanelActionsView, name='spanel'),
    path('config/<slug>/', TestConfigDetailPage.as_view(), name='config_detail'),
    
]

if os.environ.get('USE_ASGI_MODE') == 'True':
    from .views import  test_websocket_json_view, test_websocket_view

    urlpatterns += [
        path('websoccket/', test_websocket_view, name='websocket'),
        path('websoccket/json/', test_websocket_json_view, name='websocket_json'),
    ]

if os.environ.get('ENABLE_CELERY') == 'True':
    from .views import  delete_celery_tasks, test_celery_view
    urlpatterns += [
        path('celery/', test_celery_view, name='celery'),
        path('celery/task/delete', delete_celery_tasks, name='delete_celery_task'),
    ]