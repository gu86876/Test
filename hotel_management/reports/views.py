from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import date, timedelta
from bookings.models import Booking, CheckOutRecord, CheckInRecord
from rooms.models import Room
from customers.models import Customer

@login_required
def daily_report(request):
    today = date.today()
    offset = request.GET.get("offset", 0)
    try:
        offset = int(offset)
    except:
        offset = 0
    report_date = today + timedelta(days=offset)

    checkins = CheckInRecord.objects.filter(check_in_time__date=report_date).count()
    checkouts = CheckOutRecord.objects.filter(check_out_time__date=report_date)

    total_checkouts = checkouts.count()
    revenue = checkouts.aggregate(Sum("final_amount"))["final_amount__sum"] or 0
    room_revenue = checkouts.aggregate(Sum("room_charge"))["room_charge__sum"] or 0
    extra_revenue = checkouts.aggregate(Sum("extra_charges"))["extra_charges__sum"] or 0

    total_rooms = Room.objects.count()
    occupied_count = Room.objects.filter(status="occupied").count()
    occupancy_rate = round(occupied_count / total_rooms * 100, 1) if total_rooms > 0 else 0

    new_bookings = Booking.objects.filter(created_at__date=report_date).count()
    cancelled = Booking.objects.filter(status="cancelled", updated_at__date=report_date).count()

    channel_data = Booking.objects.filter(
        created_at__date=report_date
    ).values("channel").annotate(count=Count("id"), total=Sum("total_amount"))

    context = {
        "report_date": report_date,
        "offset": offset,
        "checkins": checkins,
        "total_checkouts": total_checkouts,
        "revenue": revenue,
        "room_revenue": room_revenue,
        "extra_revenue": extra_revenue,
        "occupancy_rate": occupancy_rate,
        "new_bookings": new_bookings,
        "cancelled": cancelled,
        "channel_data": channel_data,
        "total_rooms": total_rooms,
        "occupied_count": occupied_count,
    }
    return render(request, "reports/daily_report.html", context)

@login_required
def monthly_report(request):
    today = date.today()
    year = request.GET.get("year", today.year)
    month = request.GET.get("month", today.month)
    try:
        year = int(year)
        month = int(month)
    except:
        year, month = today.year, today.month

    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    start = date(year, month, 1)
    end = date(year, month, last_day)

    checkouts = CheckOutRecord.objects.filter(check_out_time__date__gte=start, check_out_time__date__lte=end)

    total_checkouts = checkouts.count()
    revenue = checkouts.aggregate(Sum("final_amount"))["final_amount__sum"] or 0
    room_revenue = checkouts.aggregate(Sum("room_charge"))["room_charge__sum"] or 0
    extra_revenue = checkouts.aggregate(Sum("extra_charges"))["extra_charges__sum"] or 0

    total_rooms = Room.objects.count()
    days_in_month = last_day
    if total_rooms > 0:
        avg_occupancy = round(total_checkouts / (total_rooms * days_in_month) * 100, 1)
        adr = round(room_revenue / total_checkouts, 2) if total_checkouts > 0 else 0
        revpar = round(revenue / (total_rooms * days_in_month), 2) if total_rooms > 0 else 0
    else:
        avg_occupancy = 0
        adr = 0
        revpar = 0

    channel_data = Booking.objects.filter(
        created_at__date__gte=start, created_at__date__lte=end
    ).values("channel").annotate(count=Count("id"), total=Sum("total_amount"))

    new_customers = Customer.objects.filter(created_at__date__gte=start, created_at__date__lte=end).count()

    context = {
        "year": year, "month": month,
        "total_checkouts": total_checkouts,
        "revenue": revenue,
        "room_revenue": room_revenue,
        "extra_revenue": extra_revenue,
        "avg_occupancy": avg_occupancy,
        "adr": adr,
        "revpar": revpar,
        "channel_data": channel_data,
        "new_customers": new_customers,
    }
    return render(request, "reports/monthly_report.html", context)

@login_required
def revenue_analysis(request):
    today = date.today()
    last_30 = today - timedelta(days=30)

    daily_revenue = []
    for i in range(30):
        d = last_30 + timedelta(days=i+1)
        rev = CheckOutRecord.objects.filter(check_out_time__date=d).aggregate(Sum("final_amount"))["final_amount__sum"] or 0
        daily_revenue.append({"date": d.strftime("%m-%d"), "revenue": float(rev)})

    top_customers = Customer.objects.annotate(
        total_spent=Sum("booking__checkoutrecord__final_amount")
    ).order_by("-total_spent")[:10]

    context = {
        "daily_revenue": daily_revenue,
        "top_customers": top_customers,
    }
    return render(request, "reports/revenue_analysis.html", context)
