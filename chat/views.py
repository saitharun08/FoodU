from django.http import JsonResponse
from .models import ChatMessage
from orders.models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def history(request, booking_id):
    booking = Booking.objects.filter(id=booking_id).first()
    if not booking or (request.user != booking.customer and request.user != booking.partner):
        return JsonResponse({'messages': []})
    qs = ChatMessage.objects.filter(booking=booking).order_by('timestamp')
    messages = [{'message': m.message, 'sender_mobile': m.sender.mobile, 'timestamp': m.timestamp.isoformat(), 'sender_id': m.sender.id} for m in qs]
    return JsonResponse({'messages': messages})
