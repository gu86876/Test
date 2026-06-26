from django.contrib import admin
from .models import RoomType, Room, RoomItem

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "base_price", "weekend_price", "capacity", "bed_type"]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_number", "floor", "room_type", "status", "current_price"]
    list_filter = ["status", "floor", "room_type"]
    search_fields = ["room_number"]

@admin.register(RoomItem)
class RoomItemAdmin(admin.ModelAdmin):
    list_display = ["room", "name", "category", "quantity", "status"]
    list_filter = ["category", "status"]
