from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/pos/', consumers.PointOfSale.as_asgi()),
    path('ws/scan/', consumers.BCScaning.as_asgi())
]