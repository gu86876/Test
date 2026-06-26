from django.urls import path
from . import views

app_name = "system"
urlpatterns = [
    path("dicts/", views.dict_list, name="dict_list"),
    path("dicts/create/", views.dict_create, name="dict_create"),
    path("dicts/<int:pk>/delete/", views.dict_delete, name="dict_delete"),
    path("logs/", views.operation_logs, name="operation_logs"),
    path("config/", views.hotel_config, name="hotel_config"),
]
