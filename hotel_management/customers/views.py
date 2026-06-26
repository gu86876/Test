from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Customer, MembershipLevel
from .forms import CustomerForm, MembershipForm
from bookings.models import Booking
from hotel_management.utils import log_operation

@login_required
def customer_list(request):
    q = request.GET.get("q", "")
    customers = Customer.objects.select_related("membership").all()
    if q:
        customers = customers.filter(name__icontains=q) | customers.filter(phone__icontains=q) | customers.filter(id_card__icontains=q)
    return render(request, "customers/customer_list.html", {"customers": customers, "q": q})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer.objects.select_related("membership"), pk=pk)
    bookings = Booking.objects.filter(customer=customer).order_by("-created_at")
    return render(request, "customers/customer_detail.html", {"customer": customer, "bookings": bookings})

@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            log_operation(request.user, "创建客户", f"创建客户: {customer.name}", request)
            messages.success(request, "客户创建成功")
            return redirect("customers:customer_list")
    else:
        form = CustomerForm()
    return render(request, "customers/customer_form.html", {"form": form, "action": "创建"})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            log_operation(request.user, "编辑客户", f"编辑客户: {customer.name}", request)
            messages.success(request, "客户更新成功")
            return redirect("customers:customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/customer_form.html", {"form": form, "action": "编辑"})

@login_required
def customer_blacklist(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.is_blacklisted = not customer.is_blacklisted
    customer.save()
    status = "拉黑" if customer.is_blacklisted else "解除拉黑"
    log_operation(request.user, status, f"{status}客户: {customer.name}", request)
    messages.success(request, f"客户已{status}")
    return redirect("customers:customer_list")

@login_required
def membership_list(request):
    levels = MembershipLevel.objects.all()
    return render(request, "customers/membership_list.html", {"levels": levels})

@login_required
def membership_create(request):
    if request.method == "POST":
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            log_operation(request.user, "创建会员等级", f"创建: {form.cleaned_data['name']}", request)
            messages.success(request, "会员等级创建成功")
            return redirect("customers:membership_list")
    else:
        form = MembershipForm()
    return render(request, "customers/membership_form.html", {"form": form, "action": "创建"})

@login_required
def membership_edit(request, pk):
    level = get_object_or_404(MembershipLevel, pk=pk)
    if request.method == "POST":
        form = MembershipForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            log_operation(request.user, "编辑会员等级", f"编辑: {level.name}", request)
            messages.success(request, "会员等级更新成功")
            return redirect("customers:membership_list")
    else:
        form = MembershipForm(instance=level)
    return render(request, "customers/membership_form.html", {"form": form, "action": "编辑"})
