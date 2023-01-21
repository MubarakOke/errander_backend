from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class LocationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room= self.scope['url_route']['kwargs']['id']
        self.room_name= f"order_{self.room}"
        self.room_name= "order"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        print(f"{self.channel_name} don connect o")
    
    async def disconnet(self):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive_json(self, content):
        coordinates= content['coordinates']
        await self.channel_layer.group_send(self.room_name,
                                            {
                                                'type':'coordinate_points',
                                                'coordinates':coordinates,
                                            }
                                            )
    
    async def coordinate_points(self, event):
        print(f"id {self.channel_name} message {event['coordinates']}")
        coordinates= event['coordinates']
        await self.send_json(content={'coordinates': coordinates})
