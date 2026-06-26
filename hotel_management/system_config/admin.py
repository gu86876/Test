from django.contrib import admin
from .models import SystemDict, OperationLog, HotelConfig

@admin.register(SystemDict)
class SystemDictAdmin(admin.ModelAdmin):
    list_display = ["category", "key", "value", "sort_order", "is_active"]
    list_filter = ["category", "is_active"]

@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "ip_address", "created_at"]
    list_filter = ["action", "created_at"]
    readonly_fields = ["user", "action", "content", "ip_address", "created_at"]

@admin.register(HotelConfig)
class HotelConfigAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "updated_at"]
