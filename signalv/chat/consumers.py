from asgiref.sync import async_to_sync

from json import dumps as json_dumps, loads as json_loads

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'something'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json_loads(text_data)

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'new_message',
            'content': data.get('message')
        })

    def new_message(self, event):
        content = event['content']

        self.send(text_data=json_dumps({
            'type': 'new_message',
            'content': content
        }))
