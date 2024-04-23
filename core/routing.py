from django.urls import path
import os

websocket_urlpatterns = []

if os.environ.get('USE_ASGI_MODE') == 'True' and os.environ.get('ENABLE_TEST_PANEL') == 'True':
    from test_app.consumers import ConnectionTestConsumer, CoordinateShareConsumer

    websocket_urlpatterns += [
        path('ws/v1/coordinates', CoordinateShareConsumer.as_asgi()),
        path('ws/connection/test', ConnectionTestConsumer.as_asgi()),
    ]


