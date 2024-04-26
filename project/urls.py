from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from project.config import PROJECT_TITLE, PUBLIC_DOMAIN, ADMIN_EMAIL, CURRENT_VERSION, COMPANY_NAME, ENABLE_TEST_PANEL, ENABLE_SWAGGER
from utils.functions import CURRENT_YEAR


public_urls = [
    path('v1/', include('accounts.urls')),
    # path('core/v1/', include('core.urls')), 
]
private_urls = [
    path('admin/', admin.site.urls),
]



urlpatterns = public_urls + private_urls
if ENABLE_TEST_PANEL:
    urlpatterns += path('test/admin/', include('test_app.urls')),

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if ENABLE_SWAGGER:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    schema_view = get_schema_view(
        openapi.Info(
            title=PROJECT_TITLE,
            default_version=CURRENT_VERSION,
            description=f"Public Domain: {PUBLIC_DOMAIN}",
            contact=openapi.Contact(email=ADMIN_EMAIL),
            license=openapi.License(name=f"{COMPANY_NAME} © {CURRENT_YEAR}. All Rights Reserved."),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    swagger_urls = [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('swagger/api.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
    urlpatterns += swagger_urls