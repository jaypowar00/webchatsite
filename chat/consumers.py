from channels.generic.websocket import AsyncWebsocketConsumer
import json
from webchatsite import settings


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if self.room_name in settings.connected_users:
            settings.connected_users[self.room_name] += 1
        else:
            settings.connected_users[self.room_name] = 1

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connected_count',
                'connected': settings.connected_users[self.room_name],
            }
        )

    async def connected_count(self, event):
        tester = event['connected']

        await self.send(text_data=json.dumps({
            'connected': tester,
        }))

    async def disconnect(self, code):
        settings.connected_users[self.room_name] -= 1

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'connected_count',
                'connected': settings.connected_users[self.room_name],
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': f'echo: {text_data}',
            }
        )

    async def chatroom_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

    pass
