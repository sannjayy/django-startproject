from django.urls import path

from test_app.consumers import ConnectionTestConsumer, CoordinateShareConsumer

websocket_urlpatterns = [
    path('ws/v1/coordinates', CoordinateShareConsumer.as_asgi()),
    path('ws/connection/test', ConnectionTestConsumer.as_asgi()),
]

