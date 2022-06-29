from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r'sig/chn/(?P<code>\d{6})/', consumers.Signaling.as_asgi(), name='signal'),
]