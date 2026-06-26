from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Role
from .forms import LoginForm, UserForm, UserProfileForm, RoleForm
from hotel_management.utils import log_operation

def is_admin(user):
    try:
        return user.profile.role and user.profile.role.code == "admin"
    except:
        return False

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            log_operation(user, "登录", "用户登录系统", request)
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):
    if request.user.is_authenticated:
        log_operation(request.user, "登出", "用户退出系统", request)
    logout(request)
    return redirect("accounts:login")

@login_required
def profile(request):
    return render(request, "accounts/profile.html")

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related("profile__role").all().order_by("-date_joined")
    return render(request, "accounts/user_list.html", {"users": users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == "POST":
        uform = UserForm(request.POST)
        pform = UserProfileForm(request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            if uform.cleaned_data.get("password"):
                user.set_password(uform.cleaned_data["password"])
            user.save()
            profile = pform.save(commit=False)
            profile.user = user
            profile.role = pform.cleaned_data.get("role")
            profile.save()
            log_operation(request.user, "创建用户", f"创建用户: {user.username}", request)
            messages.success(request, "用户创建成功")
            return redirect("accounts:user_list")
    else:
        uform = UserForm()
        pform = UserProfileForm()
    return render(request, "accounts/user_form.html", {"uform": uform, "pform": pform, "action": "创建"})

@login_required
@user_passes_test(is_admin)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = user.profile if hasattr(user, 'profile') else None
    if request.method == "POST":
        uform = UserForm(request.POST, instance=user)
        pform = UserProfileForm(request.POST, instance=profile)
        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            if uform.cleaned_data.get("password"):
                user.set_password(uform.cleaned_data["password"])
            user.save()
            p = pform.save(commit=False)
            p.user = user
            p.save()
            log_operation(request.user, "编辑用户", f"编辑用户: {user.username}", request)
            messages.success(request, "用户更新成功")
            return redirect("accounts:user_list")
    else:
        uform = UserForm(instance=user)
        pform = UserProfileForm(instance=profile)
    return render(request, "accounts/user_form.html", {"uform": uform, "pform": pform, "action": "编辑"})

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "不能删除自己")
        return redirect("accounts:user_list")
    log_operation(request.user, "删除用户", f"删除用户: {user.username}", request)
    user.delete()
    messages.success(request, "用户已删除")
    return redirect("accounts:user_list")

@login_required
@user_passes_test(is_admin)
def role_list(request):
    roles = Role.objects.all()
    return render(request, "accounts/role_list.html", {"roles": roles})

@login_required
@user_passes_test(is_admin)
def role_create(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            log_operation(request.user, "创建角色", f"创建角色: {form.cleaned_data['name']}", request)
            messages.success(request, "角色创建成功")
            return redirect("accounts:role_list")
    else:
        form = RoleForm()
    return render(request, "accounts/role_form.html", {"form": form, "action": "创建"})

@login_required
@user_passes_test(is_admin)
def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            log_operation(request.user, "编辑角色", f"编辑角色: {role.name}", request)
            messages.success(request, "角色更新成功")
            return redirect("accounts:role_list")
    else:
        form = RoleForm(instance=role)
    return render(request, "accounts/role_form.html", {"form": form, "action": "编辑"})
