from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('bookings.urls')),
    path('customers/', include('customers.urls')),
    path('reports/', include('reports.urls')),
    path('system/', include('system_config.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
