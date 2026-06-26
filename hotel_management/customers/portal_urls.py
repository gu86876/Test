from django.urls import path
from . import portal_views

app_name = "portal"
urlpatterns = [
    path("", portal_views.portal_index, name="index"),
    path("login/", portal_views.portal_login, name="login"),
    path("register/", portal_views.portal_register, name="register"),
    path("logout/", portal_views.portal_logout, name="logout"),
    path("rooms/", portal_views.portal_rooms, name="rooms"),
    path("book/<int:pk>/", portal_views.portal_book, name="book"),
    path("orders/", portal_views.portal_orders, name="orders"),
    path("orders/<int:pk>/", portal_views.portal_order_detail, name="order_detail"),
    path("orders/<int:pk>/cancel/", portal_views.portal_cancel, name="cancel"),
    path("profile/", portal_views.portal_profile, name="profile"),
]
