import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Message , Patient , Notification
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from core.serializers import NotificationSerializer

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("here")
        print(self.scope['user'].username)
        print("NON")
        self.room_name = "{}_{}".format(self.scope['url_route']['kwargs']['first'] , self.scope['url_route']['kwargs']['last'])
        print(self.scope['user'].username)

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message
            }
        )

    
    async def chat_message(self , event):
        message = event['message']
        sender = self.scope["user"].username
        receiver = self.scope['url_route']['kwargs']['first'] if sender == self.scope['url_route']['kwargs']['last'] else self.scope['url_route']['kwargs']['last']
        await self.post_message(sender = sender , receiver = receiver , message = message)
        await self.send(text_data = json.dumps({'message': message})) 

    @database_sync_to_async
    def post_message(self , sender  , receiver , message):
        sender = User.objects.filter(username = sender)[0]
        receiver = User.objects.filter(username = sender)[0]
        Message.objects.create(sender = sender , receiver = receiver , text = message)



class NotifConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name  =  'notif_{}'.format(self.scope['user'].username)
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        q = await database_sync_to_async(self.get_notif)()
        print(q)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type' : 'notifications',
                'notification' : q
            }
        )

        await self.accept

    def get_notif(self):
        print("hiii")
        print(self.scope['user'].username)
        return NotificationSerializer(Notification.objects.all().filter(user__username = self.scope['user'].username , viewed = False) , many=True).data
    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type' : 'notification',
                'notification' : 'notification'
            }
        )

    async def notification(self , event):
        notif = event['notification']
        await self.send(text_data=json.dumps({
            'notification' : notif
        }))
