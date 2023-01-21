from django.contrib import admin
from django.urls import path, re_path

from operations.consumer import LocationConsumer

websocket_urlpatterns = [
    re_path(r'^order/(?P<id>\d+)/$', LocationConsumer.as_asgi()),
]