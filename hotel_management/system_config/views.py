from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SystemDict, OperationLog, HotelConfig
from hotel_management.utils import log_operation

@login_required
def dict_list(request):
    category = request.GET.get("category", "")
    dicts = SystemDict.objects.all()
    if category:
        dicts = dicts.filter(category=category)
    return render(request, "system_config/dict_list.html", {
        "dicts": dicts, "category": category,
        "categories": SystemDict.CATEGORY_CHOICES,
    })

@login_required
def dict_create(request):
    if request.method == "POST":
        from .models import SystemDict
        d = SystemDict(
            category=request.POST.get("category"),
            key=request.POST.get("key"),
            value=request.POST.get("value"),
            sort_order=request.POST.get("sort_order", 0),
            description=request.POST.get("description", ""),
        )
        d.save()
        messages.success(request, "字典项添加成功")
        return redirect("system:dict_list")
    return redirect("system:dict_list")

@login_required
def dict_delete(request, pk):
    d = get_object_or_404(SystemDict, pk=pk)
    d.delete()
    messages.success(request, "字典项已删除")
    return redirect("system:dict_list")

@login_required
def operation_logs(request):
    action = request.GET.get("action", "")
    logs = OperationLog.objects.select_related("user").all()
    if action:
        logs = logs.filter(action=action)
    actions = OperationLog.objects.values_list("action", flat=True).distinct()
    return render(request, "system_config/log_list.html", {
        "logs": logs, "action_filter": action, "actions": actions
    })

@login_required
def hotel_config(request):
    configs = HotelConfig.objects.all()
    if request.method == "POST":
        key = request.POST.get("key")
        value = request.POST.get("value")
        desc = request.POST.get("description", "")
        config, created = HotelConfig.objects.update_or_create(
            key=key, defaults={"value": value, "description": desc}
        )
        messages.success(request, "配置已保存")
        return redirect("system:hotel_config")
    return render(request, "system_config/hotel_config.html", {"configs": configs})
