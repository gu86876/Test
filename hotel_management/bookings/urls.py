from django.urls import path
from . import views

app_name = "bookings"
urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("create/", views.booking_create, name="booking_create"),
    path("<int:pk>/", views.booking_detail, name="booking_detail"),
    path("<int:pk>/cancel/", views.booking_cancel, name="booking_cancel"),
    path("check-in/", views.check_in, name="check_in"),
    path("check-in/walk-in/", views.check_in_walk_in, name="check_in_walk_in"),
    path("check-out/", views.check_out, name="check_out"),
    path("room-change/", views.room_change, name="room_change"),
]
