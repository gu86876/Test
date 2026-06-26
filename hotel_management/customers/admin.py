from django.contrib import admin
from .models import MembershipLevel, Customer

@admin.register(MembershipLevel)
class MembershipLevelAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "discount", "points_rate", "late_checkout_hours"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "id_card", "membership", "points", "total_stays", "is_blacklisted"]
    list_filter = ["membership", "is_blacklisted", "gender"]
    search_fields = ["name", "phone", "id_card"]
