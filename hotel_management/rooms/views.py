from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RoomType, Room, RoomItem
from .forms import RoomTypeForm, RoomForm, RoomItemForm
from hotel_management.utils import log_operation

@login_required
def room_grid(request):
    rooms = Room.objects.select_related("room_type").all().order_by("floor", "room_number")
    room_types = RoomType.objects.all()
    status_filter = request.GET.get("status", "")
    floor_filter = request.GET.get("floor", "")
    type_filter = request.GET.get("type", "")
    if status_filter:
        rooms = rooms.filter(status=status_filter)
    if floor_filter:
        rooms = rooms.filter(floor=floor_filter)
    if type_filter:
        rooms = rooms.filter(room_type_id=type_filter)
    floors = sorted(set(Room.objects.values_list("floor", flat=True)))
    context = {
        "rooms": rooms,
        "room_types": room_types,
        "floors": floors,
        "status_filter": status_filter,
        "floor_filter": floor_filter,
        "type_filter": type_filter,
        "status_choices": Room.STATUS_CHOICES,
    }
    return render(request, "rooms/room_grid.html", context)

@login_required
def room_list(request):
    rooms = Room.objects.select_related("room_type").all().order_by("floor", "room_number")
    return render(request, "rooms/room_list.html", {"rooms": rooms})

@login_required
def room_create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            log_operation(request.user, "创建房间", f"创建房间: {room.room_number}", request)
            messages.success(request, "房间创建成功")
            return redirect("rooms:room_grid")
    else:
        form = RoomForm()
    return render(request, "rooms/room_form.html", {"form": form, "action": "创建"})

@login_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            log_operation(request.user, "编辑房间", f"编辑房间: {room.room_number}", request)
            messages.success(request, "房间更新成功")
            return redirect("rooms:room_grid")
    else:
        form = RoomForm(instance=room)
    return render(request, "rooms/room_form.html", {"form": form, "action": "编辑"})

@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    log_operation(request.user, "删除房间", f"删除房间: {room.room_number}", request)
    room.delete()
    messages.success(request, "房间已删除")
    return redirect("rooms:room_grid")

@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room.objects.select_related("room_type").prefetch_related("items"), pk=pk)
    return render(request, "rooms/room_detail.html", {"room": room})

@login_required
def room_type_list(request):
    types = RoomType.objects.all()
    return render(request, "rooms/room_type_list.html", {"types": types})

@login_required
def room_type_create(request):
    if request.method == "POST":
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            form.save()
            log_operation(request.user, "创建房型", f"创建房型: {form.cleaned_data['name']}", request)
            messages.success(request, "房型创建成功")
            return redirect("rooms:room_type_list")
    else:
        form = RoomTypeForm()
    return render(request, "rooms/room_type_form.html", {"form": form, "action": "创建"})

@login_required
def room_type_edit(request, pk):
    rt = get_object_or_404(RoomType, pk=pk)
    if request.method == "POST":
        form = RoomTypeForm(request.POST, instance=rt)
        if form.is_valid():
            form.save()
            log_operation(request.user, "编辑房型", f"编辑房型: {rt.name}", request)
            messages.success(request, "房型更新成功")
            return redirect("rooms:room_type_list")
    else:
        form = RoomTypeForm(instance=rt)
    return render(request, "rooms/room_type_form.html", {"form": form, "action": "编辑"})

@login_required
def room_item_manage(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    items = room.items.all()
    if request.method == "POST":
        form = RoomItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.room = room
            item.save()
            messages.success(request, "物品添加成功")
            return redirect("rooms:room_item_manage", room_pk=room.pk)
    else:
        form = RoomItemForm(initial={"room": room})
    return render(request, "rooms/room_item_manage.html", {"room": room, "items": items, "form": form})

@login_required
def update_room_status(request, pk, status):
    room = get_object_or_404(Room, pk=pk)
    valid_statuses = [s[0] for s in Room.STATUS_CHOICES]
    if status in valid_statuses:
        old_status = room.get_status_display()
        room.status = status
        room.save()
        log_operation(request.user, "更改房态", f"房间{room.room_number}: {old_status} -> {room.get_status_display()}", request)
        messages.success(request, f"房间{room.room_number}状态已更新为{room.get_status_display()}")
    return redirect("rooms:room_grid")
