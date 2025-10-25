import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage
from orders.models import Booking

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = f"chat_{self.booking_id}"

        # Ensure user is authenticated
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        # Ensure booking exists and user is either customer or assigned partner
        booking = await database_sync_to_async(self.get_booking)()
        if not booking:
            await self.close()
            return

        if not (user == booking.customer or user == booking.partner):
            await self.close()
            return

        # Only allow chat when booking assigned (or later)
        if booking.status == 'created' or booking.partner is None:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    def get_booking(self):
        try:
            return Booking.objects.select_related('customer', 'partner').get(id=self.booking_id)
        except Booking.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        if not message:
            return

        user = self.scope['user']
        # Save message to DB
        chat_obj = await database_sync_to_async(self.create_message)(user, message)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": chat_obj.message,
                "sender_mobile": user.mobile,
                "timestamp": chat_obj.timestamp.isoformat(),
                "sender_id": user.id,
            }
        )

    def create_message(self, user, message):
        booking = Booking.objects.get(id=self.booking_id)
        return ChatMessage.objects.create(booking=booking, sender=user, message=message)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_mobile": event["sender_mobile"],
            "timestamp": event["timestamp"],
            "sender_id": event["sender_id"],
        }))
