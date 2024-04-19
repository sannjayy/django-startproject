import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
application = get_asgi_application()


if os.environ.get('USE_ASGI_MODE') == 'True':
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    from core.routing import websocket_urlpatterns
    application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
            )
        )
    })
