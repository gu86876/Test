import os
base = r"D:\Test_git\hotel_management"

# ===== CUSTOMER PORTAL VIEWS =====
portal_views = '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Q
from .models import Customer, MembershipLevel
from rooms.models import Room, RoomType
from bookings.models import Booking, CheckInRecord
from hotel_management.utils import calculate_price

def portal_login(request):
    if request.session.get("customer_id"):
        return redirect("portal:index")
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        try:
            customer = Customer.objects.get(phone=phone, is_active=True)
            if not customer.password:
                customer.password = make_password("123456")
                customer.save()
            if check_password(password, customer.password):
                request.session["customer_id"] = customer.pk
                request.session["customer_name"] = customer.name
                messages.success(request, f"欢迎回来，{customer.name}！")
                return redirect("portal:index")
            else:
                messages.error(request, "密码错误")
        except Customer.DoesNotExist:
            messages.error(request, "账号不存在")
    return render(request, "portal/login.html")

def portal_register(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        if not all([name, phone, password]):
            messages.error(request, "请填写所有必填项")
        elif password != password2:
            messages.error(request, "两次密码不一致")
        elif Customer.objects.filter(phone=phone).exists():
            messages.error(request, "该手机号已注册")
        else:
            customer = Customer.objects.create(
                name=name, phone=phone,
                password=make_password(password),
            )
            request.session["customer_id"] = customer.pk
            request.session["customer_name"] = customer.name
            messages.success(request, f"注册成功，欢迎 {name}！")
            return redirect("portal:index")
    return render(request, "portal/register.html")

def portal_logout(request):
    request.session.pop("customer_id", None)
    request.session.pop("customer_name", None)
    return redirect("portal:login")

def get_customer(request):
    cid = request.session.get("customer_id")
    if cid:
        return Customer.objects.select_related("membership").filter(pk=cid).first()
    return None

def require_customer(view_func):
    def wrapper(request, *args, **kwargs):
        customer = get_customer(request)
        if not customer:
            return redirect("portal:login")
        request.customer = customer
        return view_func(request, *args, **kwargs)
    return wrapper

@require_customer
def portal_index(request):
    room_types = RoomType.objects.all()
    available_count = Room.objects.filter(status="available").count()
    return render(request, "portal/index.html", {
        "room_types": room_types,
        "available_count": available_count,
        "customer": request.customer,
    })

@require_customer
def portal_rooms(request):
    type_id = request.GET.get("type", "")
    rooms = Room.objects.select_related("room_type").filter(status="available")
    if type_id:
        rooms = rooms.filter(room_type_id=type_id)
    room_types = RoomType.objects.all()
    return render(request, "portal/rooms.html", {
        "rooms": rooms,
        "room_types": room_types,
        "type_filter": type_id,
        "customer": request.customer,
    })

@require_customer
def portal_book(request, pk):
    room = get_object_or_404(Room.objects.select_related("room_type"), pk=pk, status="available")
    if request.method == "POST":
        check_in = request.POST.get("check_in", "")
        check_out = request.POST.get("check_out", "")
        if not check_in or not check_out:
            messages.error(request, "请选择入住和离店日期")
        else:
            ci = date.fromisoformat(check_in)
            co = date.fromisoformat(check_out)
            if ci >= co:
                messages.error(request, "离店日期必须晚于入住日期")
            elif ci < date.today():
                messages.error(request, "入住日期不能早于今天")
            else:
                days = (co - ci).days
                total = calculate_price(room, ci, co)
                booking = Booking.objects.create(
                    customer=request.customer,
                    room=room,
                    room_type_name=room.room_type.name,
                    check_in_date=ci,
                    check_out_date=co,
                    guest_count=request.POST.get("guests", 1),
                    total_amount=total,
                    channel="online",
                    status="confirmed",
                    notes=request.POST.get("notes", ""),
                )
                room.status = "reserved"
                room.save()
                messages.success(request, f"预订成功！订单号: {booking.order_no}，金额: ¥{total}")
                return redirect("portal:orders")
    return render(request, "portal/book.html", {
        "room": room,
        "customer": request.customer,
        "today": date.today().isoformat(),
    })

@require_customer
def portal_orders(request):
    orders = Booking.objects.filter(customer=request.customer).order_by("-created_at")
    return render(request, "portal/orders.html", {
        "orders": orders,
        "customer": request.customer,
    })

@require_customer
def portal_order_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.customer)
    try:
        check_in = booking.checkinrecord
    except:
        check_in = None
    try:
        from bookings.models import CheckOutRecord
        check_out = CheckOutRecord.objects.filter(booking=booking).first()
    except:
        check_out = None
    return render(request, "portal/order_detail.html", {
        "booking": booking,
        "check_in": check_in,
        "check_out": check_out,
        "customer": request.customer,
    })

@require_customer
def portal_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.customer)
    if booking.status in ["pending", "confirmed"]:
        booking.status = "cancelled"
        booking.save()
        if booking.room:
            booking.room.status = "available"
            booking.room.save()
        messages.success(request, "订单已取消")
    else:
        messages.error(request, "当前状态不可取消")
    return redirect("portal:orders")

@require_customer
def portal_profile(request):
    customer = request.customer
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        birthday = request.POST.get("birthday", "")
        preferences = request.POST.get("preferences", "")
        customer.name = name
        customer.email = email
        if birthday:
            customer.birthday = date.fromisoformat(birthday)
        customer.preferences = preferences
        customer.save()

        new_pwd = request.POST.get("new_password", "")
        if new_pwd:
            if new_pwd == request.POST.get("new_password2", ""):
                customer.password = make_password(new_pwd)
                customer.save()
                messages.success(request, "密码已更新")
            else:
                messages.error(request, "两次密码不一致")
        messages.success(request, "个人信息已更新")
        return redirect("portal:profile")
    return render(request, "portal/profile.html", {
        "customer": customer,
    })
'''

with open(os.path.join(base, "customers", "portal_views.py"), "w", encoding="utf-8") as f:
    f.write(portal_views)
print("portal_views.py OK")
