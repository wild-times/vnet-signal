from dataclasses import dataclass

from channels.generic.websocket import AsyncJsonWebsocketConsumer


@dataclass
class SignalTypes:
    SIGNAL_CONNECTED = 'signal_connected'
    SIGNAL_DISCONNECTED = 'signal_disconnected'
    OFFER = 'offer'
    ANSWER = 'answer'
    CANDIDATES = 'candidates'


# noinspection PyStatementEffect
class Signaling(AsyncJsonWebsocketConsumer):
    signal_types = SignalTypes()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_code, self.channel_name)
        await self.channel_layer.group_send(self.room_code, {
            'type': 'signal_assure',
            'content': {
                'type': self.signal_types.SIGNAL_DISCONNECTED,
                'code': self.room_code,
                'peers_count': len(self.channel_layer.groups.get(self.room_code, {}).items()),
            }
        })

    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['code']
        room_mem = len(self.channel_layer.groups.get(self.room_code, {}).items())

        if room_mem < 2:
            await self.channel_layer.group_add(self.room_code, self.channel_name)
            await self.accept()

            await self.channel_layer.group_send(self.room_code, {
                'type': 'signal_assure',
                'content': {
                    'type': self.signal_types.SIGNAL_CONNECTED,
                    'code': self.room_code,
                    'peers_count': room_mem + 1,
                }
            })

    async def receive_json(self, content, **kwargs):
        if type(content) == dict and content.get('type') and content.get('content'):
            type_ = content.get('type')
            _content = {
                'type': type_,
                'sdp' if type_ in ['offer', 'answer'] else 'candidates': content.get('content')
            }

            await self.channel_layer.group_send(self.room_code, {
                'type': 'signal_message',
                'code': self.room_code,
                'content': _content
            })

    async def signal_assure(self, event):
        await self.send_json(event.get('content'))

    async def signal_message(self, event):
        await self.send_json(event.get('content'))
