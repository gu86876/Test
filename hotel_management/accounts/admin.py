from django.contrib import admin
from .models import Role, UserProfile

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "created_at"]
    search_fields = ["name", "code"]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "phone", "is_active_staff", "created_at"]
    list_filter = ["role", "is_active_staff"]
    search_fields = ["user__username", "phone"]
