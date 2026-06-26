from django.contrib import admin
from .models import Booking, CheckInRecord, CheckOutRecord

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["order_no", "customer", "room", "check_in_date", "check_out_date", "status", "total_amount", "channel"]
    list_filter = ["status", "channel", "check_in_date"]
    search_fields = ["order_no", "customer__name"]

@admin.register(CheckInRecord)
class CheckInRecordAdmin(admin.ModelAdmin):
    list_display = ["booking", "room", "check_in_time", "deposit_amount", "staff"]

@admin.register(CheckOutRecord)
class CheckOutRecordAdmin(admin.ModelAdmin):
    list_display = ["booking", "check_out_time", "total_amount", "payment_method", "staff"]
