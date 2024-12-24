# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the user to the WebSocket group
        await self.channel_layer.group_add('notifications', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the WebSocket group
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def send_notification(self, event):
        # Send the notification data to the connected user
        notification_data = event['data']
        await self.send(text_data=json.dumps(notification_data))
