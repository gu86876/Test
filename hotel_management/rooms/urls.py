from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    path("", views.room_grid, name="room_grid"),
    path("list/", views.room_list, name="room_list"),
    path("create/", views.room_create, name="room_create"),
    path("<int:pk>/", views.room_detail, name="room_detail"),
    path("<int:pk>/edit/", views.room_edit, name="room_edit"),
    path("<int:pk>/delete/", views.room_delete, name="room_delete"),
    path("<int:pk>/items/", views.room_item_manage, name="room_item_manage"),
    path("<int:pk>/status/<str:status>/", views.update_room_status, name="update_room_status"),
    path("types/", views.room_type_list, name="room_type_list"),
    path("types/create/", views.room_type_create, name="room_type_create"),
    path("types/<int:pk>/edit/", views.room_type_edit, name="room_type_edit"),
]
