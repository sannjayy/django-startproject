from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs
from channels.exceptions import StopConsumer

#  Created By Sanjay [ Znas Solutions ]

async def send_message(self, msg, group='test_group'):
    # Send Messasge
    await self.channel_layer.group_send(group, {
        'type': 'send.notification',
        'value': msg
    })
    
    
class ConnectionTestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await(self.channel_layer.group_add)(
            'test_group',
            self.channel_name
        )
        await self.accept()
        # await self.send(text_data='Accepted your connection.')
        await send_message(self, 'Accepted new connection!')
    
    async def receive(self, text_data):
        await self.channel_layer.group_send('test_group', {
            'type': 'send.notification',
            'value': text_data
        })

    async def disconnect(self, close_code):
        await send_message(self, 'Disconnected!')
        await self.channel_layer.group_discard(
            'test_group', 
            self.channel_name
        )
        raise StopConsumer
    
    async def send_notification(self, event):
        payload = event.get('value')
        await self.send(text_data=payload)


class CoordinateShareConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):        
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        query_params = parse_qs(query_string)

        self.token = query_params.get('Token', [''])[0]
        self.user = query_params.get('User', [''])[0]
        self.label = query_params.get('Label', [''])[0]
        self.source = query_params.get('Source', [''])[0] # If from Django Don't Save Data

        if not self.token:
            await self.accept()
            await self.send_json(content={'status': "Invalid credentials - Kicked out!"})
            await self.close()

        await self.accept()
        await(self.channel_layer.group_add)(
            self.token,
            self.channel_name
        )
        await self.channel_layer.group_send(self.token, {
            'type': 'send.info',
            'value':  f"Joined {self.user or ''} on {self.token} - Socket!"
        })
        # await self.send_json(content={'status': 'Connected with Socket!'})

    
    async def receive_json(self, content, **kwargs):
        if not self.token:
            await self.send_json(content={'detail': 'You are not joined any company.'})

        else:
            # if isinstance(content, dict):
            content = {**content, 'user': self.user, 'label': self.label}
            await self.channel_layer.group_send(self.token, {
                'type': 'send.notification',
                'value': content
            })



    async def disconnect(self, close_code):
        # await self.send_group_message(self, content={'status': 'Disconnected!'})
        
        # await self.channel_layer.group_discard(
        #     self.room_group_name, 
        #     self.channel_name
        # )
        raise StopConsumer
    
    async def send_notification(self, event):
        payload = event.get('value')
        await self.send_json(content={
            'detail': 'notification',
            'payload': payload
            
        })

    async def send_info(self, event):
        payload = event.get('value')
        await self.send(text_data=payload)
        
