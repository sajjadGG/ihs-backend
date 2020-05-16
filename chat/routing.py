from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<first>\w+)/(?P<last>\w+)/$' , consumers.ChatConsumer),
    re_path(r'ws/notification/' , consumers.NotifConsumer)
]