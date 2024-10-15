# NCC/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SubmissionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.submission_id = self.scope['url_route']['kwargs']['submission_id']
        self.room_group_name = f'submission_{self.submission_id}'

        # Join submission group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave submission group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     status = text_data_json['status']

    #     # Send message to submission group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'submission_status',
    #             'status': status
    #         }
    #     )

    # Receive message from submission group
    async def submission_final_status(self, event):
        submission_data = event['submission_data']

        # Send message to WebSocket with type 'final_status'
        await self.send(text_data=json.dumps({
            'type': 'final_status',
            'submission_data': submission_data,
        }))

    async def submission_status_update(self, event):
        submission_data = event['submission_data']

        # Send status update message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'submission_data': submission_data
        }))