from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def send_notification_to_web(notification_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('notifications', {
        'type': 'send_notification',
        'data': notification_data,
    })
