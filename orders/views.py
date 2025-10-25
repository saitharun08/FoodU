from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import Booking
from .forms import BookingForm
from accounts.models import User

@role_required(['customer'])
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/customer_dashboard.html', {'bookings': bookings})

@role_required(['customer'])
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, "Booking created successfully.")
            return redirect('customer_dashboard')
    else:
        form = BookingForm()
    return render(request, 'orders/create_booking.html', {'form': form})

@role_required(['customer'])
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status == 'created':
        booking.status = 'cancelled'
        booking.save()
        messages.info(request, "Booking cancelled.")
    else:
        messages.error(request, "Cannot cancel once assigned or started.")
    return redirect('customer_dashboard')

@role_required(['admin'])
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    partners = User.objects.filter(role='partner')

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        partner_id = request.POST.get('partner_id')
        booking = Booking.objects.get(id=booking_id)
        partner = User.objects.get(id=partner_id)
        booking.partner = partner
        # Keep both fields in sync for templates that reference either
        if hasattr(booking, 'assigned_to'):
            booking.assigned_to = partner
        booking.status = 'assigned'
        booking.save()
        messages.success(request, f"Booking {booking_id} assigned to {partner.mobile}")
        return redirect('admin_dashboard')

    return render(request, 'orders/admin_dashboard.html', {'bookings': bookings, 'partners': partners})

@role_required(['partner'])
def partner_dashboard(request):
    bookings = Booking.objects.filter(partner=request.user)
    return render(request, 'orders/partner_dashboard.html', {'bookings': bookings})

@role_required(['partner'])
def update_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, partner=request.user)
    flow = ['assigned', 'started', 'reached', 'collected', 'delivered']
    current_index = flow.index(booking.status) if booking.status in flow else -1

    if current_index + 1 < len(flow):
        booking.status = flow[current_index + 1]
        booking.save()
        messages.success(request, f"Status updated to {booking.status}")
    else:
        messages.info(request, "Already delivered.")
    return redirect('partner_dashboard')

@role_required(['admin'])
def assign_partner(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        if partner_id:
            partner = User.objects.get(id=partner_id)
            booking.partner = partner
            if hasattr(booking, 'assigned_to'):
                booking.assigned_to = partner
            booking.status = 'assigned'
            booking.save()
            messages.success(request, f"Booking {booking.id} assigned to {partner.mobile}")
    return redirect('admin_dashboard')

