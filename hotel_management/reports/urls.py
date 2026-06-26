from django.urls import path
from . import views

app_name = "reports"
urlpatterns = [
    path("daily/", views.daily_report, name="daily_report"),
    path("monthly/", views.monthly_report, name="monthly_report"),
    path("revenue/", views.revenue_analysis, name="revenue_analysis"),
]
