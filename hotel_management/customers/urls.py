from django.urls import path
from . import views

app_name = "customers"
urlpatterns = [
    path("", views.customer_list, name="customer_list"),
    path("create/", views.customer_create, name="customer_create"),
    path("<int:pk>/", views.customer_detail, name="customer_detail"),
    path("<int:pk>/edit/", views.customer_edit, name="customer_edit"),
    path("<int:pk>/blacklist/", views.customer_blacklist, name="customer_blacklist"),
    path("membership/", views.membership_list, name="membership_list"),
    path("membership/create/", views.membership_create, name="membership_create"),
    path("membership/<int:pk>/edit/", views.membership_edit, name="membership_edit"),
]
