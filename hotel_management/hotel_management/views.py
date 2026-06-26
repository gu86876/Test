from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from bookings.models import Booking, CheckInRecord, CheckOutRecord
from customers.models import Customer
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date, timedelta

@login_required
def dashboard(request):
    total_rooms = Room.objects.count()
    occupied = Room.objects.filter(status='occupied').count()
    available = Room.objects.filter(status='available').count()
    dirty = Room.objects.filter(status='dirty').count()
    maintenance = Room.objects.filter(status='maintenance').count()
    reserved = Room.objects.filter(status='reserved').count()

    today = date.today()
    today_checkins = CheckInRecord.objects.filter(check_in_time__date=today).count()
    today_checkouts = CheckOutRecord.objects.filter(check_out_time__date=today).count()
    active_bookings = Booking.objects.filter(status__in=['pending','confirmed','checked_in']).count()

    total_customers = Customer.objects.count()
    total_revenue = CheckOutRecord.objects.filter(check_out_time__date=today).aggregate(Sum('final_amount'))['final_amount__sum'] or 0

    recent_checkins = CheckInRecord.objects.select_related('customer','room','booking').order_by('-check_in_time')[:10]
    recent_bookings = Booking.objects.select_related('customer','room').order_by('-created_at')[:10]

    occupancy_rate = round(occupied / total_rooms * 100, 1) if total_rooms > 0 else 0

    context = {
        'total_rooms': total_rooms,
        'occupied': occupied,
        'available': available,
        'dirty': dirty,
        'maintenance': maintenance,
        'reserved': reserved,
        'today_checkins': today_checkins,
        'today_checkouts': today_checkouts,
        'active_bookings': active_bookings,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'occupancy_rate': occupancy_rate,
        'recent_checkins': recent_checkins,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard.html', context)
