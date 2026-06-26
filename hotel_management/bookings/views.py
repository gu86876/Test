from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Booking, CheckInRecord, CheckOutRecord
from .forms import BookingForm, CheckInForm, CheckOutForm, CustomerQuickForm
from rooms.models import Room
from customers.models import Customer
from hotel_management.utils import log_operation, calculate_price

@login_required
def booking_list(request):
    status = request.GET.get("status", "")
    bookings = Booking.objects.select_related("customer", "room").all()
    if status:
        bookings = bookings.filter(status=status)
    return render(request, "bookings/booking_list.html", {
        "bookings": bookings,
        "status_filter": status,
        "status_choices": Booking.STATUS_CHOICES,
    })

@login_required
def booking_create(request):
    rooms = Room.objects.filter(status="available")
    customers = Customer.objects.filter(is_blacklisted=False)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.created_by = request.user
            if booking.room:
                booking.room_type_name = booking.room.room_type.name
                days = (booking.check_out_date - booking.check_in_date).days
                booking.total_amount = calculate_price(booking.room, booking.check_in_date, booking.check_out_date) * max(days, 1)
            booking.save()
            if booking.room:
                booking.room.status = "reserved"
                booking.room.save()
            log_operation(request.user, "创建订单", f"创建订单: {booking.order_no}", request)
            messages.success(request, f"订单 {booking.order_no} 创建成功")
            return redirect("bookings:booking_list")
    else:
        form = BookingForm()
    return render(request, "bookings/booking_form.html", {
        "form": form, "action": "创建", "rooms": rooms, "customers": customers
    })

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking.objects.select_related("customer", "room", "created_by"), pk=pk)
    try:
        check_in = booking.checkinrecord
    except:
        check_in = None
    try:
        check_out = CheckOutRecord.objects.filter(booking=booking).first()
    except:
        check_out = None
    return render(request, "bookings/booking_detail.html", {
        "booking": booking, "check_in": check_in, "check_out": check_out
    })

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = "cancelled"
    booking.save()
    if booking.room:
        booking.room.status = "available"
        booking.room.save()
    log_operation(request.user, "取消订单", f"取消订单: {booking.order_no}", request)
    messages.success(request, f"订单 {booking.order_no} 已取消")
    return redirect("bookings:booking_list")

@login_required
def check_in(request):
    pending_bookings = Booking.objects.filter(status__in=["pending", "confirmed"]).select_related("customer", "room")
    available_rooms = Room.objects.filter(status="available")
    customers = Customer.objects.filter(is_blacklisted=False)
    if request.method == "POST":
        form = CheckInForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.staff = request.user
            checkin.save()
            booking = checkin.booking
            booking.status = "checked_in"
            booking.room = checkin.room
            booking.save()
            if checkin.room:
                checkin.room.status = "occupied"
                checkin.room.save()
            customer = checkin.customer
            customer.total_stays += 1
            customer.save()
            log_operation(request.user, "办理入住", f"入住: {booking.order_no}, 房间: {checkin.room}", request)
            messages.success(request, f"入住办理成功 - {booking.order_no}")
            return redirect("bookings:booking_list")
    else:
        form = CheckInForm()
    return render(request, "bookings/check_in.html", {
        "form": form, "pending_bookings": pending_bookings,
        "available_rooms": available_rooms, "customers": customers,
    })

@login_required
def check_in_walk_in(request):
    rooms = Room.objects.filter(status="available").select_related("room_type")
    if request.method == "POST":
        cform = CustomerQuickForm(request.POST)
        if cform.is_valid():
            customer = cform.save()
            room_id = request.POST.get("room_id")
            room = get_object_or_404(Room, pk=room_id)
            check_in_date = request.POST.get("check_in_date")
            check_out_date = request.POST.get("check_out_date")
            from datetime import date
            today = date.today()
            booking = Booking.objects.create(
                customer=customer, room=room, room_type_name=room.room_type.name,
                check_in_date=today, check_out_date=check_out_date or today,
                status="checked_in", channel="walk_in", created_by=request.user,
                total_amount=calculate_price(room, today, date.fromisoformat(check_out_date) if check_out_date else today),
            )
            CheckInRecord.objects.create(
                booking=booking, customer=customer, room=room,
                deposit_amount=request.POST.get("deposit", 0),
                staff=request.user, key_card_no=request.POST.get("key_card", ""),
            )
            room.status = "occupied"
            room.save()
            customer.total_stays += 1
            customer.save()
            log_operation(request.user, "散客入住", f"散客入住: {booking.order_no}", request)
            messages.success(request, f"散客入住办理成功 - {booking.order_no}")
            return redirect("bookings:booking_list")
    else:
        cform = CustomerQuickForm()
    return render(request, "bookings/check_in_walk_in.html", {"form": cform, "rooms": rooms})

@login_required
def check_out(request):
    active_checkins = CheckInRecord.objects.filter(
        booking__status="checked_in"
    ).select_related("booking", "customer", "room").order_by("-check_in_time")

    if request.method == "POST":
        check_in_id = request.POST.get("check_in_id")
        checkin = get_object_or_404(CheckInRecord.objects.select_related("booking", "customer", "room"), pk=check_in_id)
        booking = checkin.booking

        room_charge = calculate_price(checkin.room, booking.check_in_date, booking.check_out_date) if checkin.room else 0
        extra = float(request.POST.get("extra_charges", 0))
        penalty = float(request.POST.get("penalty", 0))
        total = room_charge + extra + penalty
        deposit = float(request.POST.get("deposit_used", 0))
        final = total - deposit

        checkout = CheckOutRecord.objects.create(
            check_in_record=checkin, booking=booking, customer=checkin.customer,
            room_charge=room_charge, extra_charges=extra, penalty=penalty,
            total_amount=total, deposit_used=deposit, final_amount=max(final, 0),
            payment_method=request.POST.get("payment_method", "cash"),
            invoice_no=request.POST.get("invoice_no", ""),
            staff=request.user, notes=request.POST.get("notes", ""),
        )
        booking.status = "checked_out"
        booking.total_amount = total
        booking.save()
        if checkin.room:
            checkin.room.status = "dirty"
            checkin.room.save()
        customer = checkin.customer
        points_earned = int(total)
        if customer.membership:
            points_earned = int(total * float(customer.membership.points_rate))
        customer.points += points_earned
        customer.total_spending += total
        customer.save()
        log_operation(request.user, "办理退房", f"退房: {booking.order_no}, 实收: {max(final, 0)}", request)
        messages.success(request, f"退房办理成功! 实收: {max(final, 0):.2f}元")
        return redirect("bookings:booking_list")

    return render(request, "bookings/check_out.html", {"active_checkins": active_checkins})

@login_required
def room_change(request):
    active_checkins = CheckInRecord.objects.filter(
        booking__status="checked_in"
    ).select_related("booking", "customer", "room")
    available_rooms = Room.objects.filter(status="available")

    if request.method == "POST":
        check_in_id = request.POST.get("check_in_id")
        new_room_id = request.POST.get("new_room_id")
        checkin = get_object_or_404(CheckInRecord, pk=check_in_id)
        new_room = get_object_or_404(Room, pk=new_room_id)
        old_room = checkin.room
        if old_room:
            old_room.status = "dirty"
            old_room.save()
        checkin.room = new_room
        checkin.booking.room = new_room
        checkin.booking.save()
        checkin.save()
        new_room.status = "occupied"
        new_room.save()
        log_operation(request.user, "换房", f"订单{checkin.booking.order_no}: {old_room} -> {new_room}", request)
        messages.success(request, f"换房成功: {old_room} -> {new_room}")
        return redirect("bookings:booking_list")

    return render(request, "bookings/room_change.html", {
        "active_checkins": active_checkins, "available_rooms": available_rooms
    })
