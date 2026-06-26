import os
base = r"D:\Test_git\hotel_management"

# ===== PORTAL URLS =====
portal_urls = '''from django.urls import path
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
'''
with open(os.path.join(base, "customers", "portal_urls.py"), "w", encoding="utf-8") as f:
    f.write(portal_urls)

# ===== UPDATE MAIN URLS =====
main_urls = '''from django.contrib import admin
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
    path('portal/', include('customers.portal_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
with open(os.path.join(base, "hotel_management", "urls.py"), "w", encoding="utf-8") as f:
    f.write(main_urls)

print("URLs created")

# ===== PORTAL BASE TEMPLATE =====
portal_base = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}云璟国际酒店{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <style>
        :root {
            --gold: #c8a45c;
            --gold-light: #f5e6cc;
        }
        .portal-header {
            background: #fff;
            border-bottom: 1px solid #e5e7eb;
            padding: 0 24px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        .portal-header .logo {
            font-size: 20px;
            font-weight: 700;
            color: var(--gold);
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }
        .portal-header .logo i { font-size: 24px; }
        .portal-nav { display: flex; gap: 4px; align-items: center; }
        .portal-nav a {
            text-decoration: none;
            color: #374151;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.15s;
        }
        .portal-nav a:hover { background: #f3f4f6; }
        .portal-nav a.btn-book {
            background: var(--gold);
            color: #fff;
            padding: 10px 20px;
        }
        .portal-nav a.btn-book:hover { background: #b8941f; }
        .portal-user { display: flex; align-items: center; gap: 8px; font-size: 14px; }
        .portal-content { max-width: 1200px; margin: 0 auto; padding: 32px 24px; }
        .portal-content.no-auth { min-height: calc(100vh - 64px); display: flex; align-items: center; justify-content: center; }

        .hero { text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: #fff; border-radius: 16px; margin-bottom: 40px; }
        .hero h1 { font-size: 36px; margin-bottom: 12px; }
        .hero p { font-size: 16px; color: #94a3b8; margin-bottom: 24px; }
        .room-type-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 24px; }
        .room-type-card {
            background: #fff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e5e7eb;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }
        .room-type-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
        .room-type-card .card-img {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 160px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            color: rgba(255,255,255,0.7);
        }
        .room-type-card:nth-child(2) .card-img { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .room-type-card:nth-child(3) .card-img { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .room-type-card:nth-child(4) .card-img { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .room-type-card .card-body { padding: 16px 20px; }
        .room-type-card .card-body h3 { font-size: 18px; margin-bottom: 4px; }
        .room-type-card .card-body .price { font-size: 24px; font-weight: 700; color: #dc2626; }
        .room-type-card .card-body .price span { font-size: 14px; color: #64748b; font-weight: 400; }

        .section-title { font-size: 22px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .order-card {
            background: #fff;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            padding: 20px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .order-card .order-info { flex: 1; min-width: 200px; }
        .order-card .order-no { font-weight: 600; font-size: 15px; }
        .order-card .order-meta { font-size: 13px; color: #64748b; margin-top: 4px; }
        .order-card .order-amount { text-align: right; }
        .order-card .order-amount .price { font-size: 20px; font-weight: 700; color: #dc2626; }
        .login-card { background: #fff; border-radius: 16px; padding: 40px; width: 400px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); }
        .login-card h2 { text-align: center; margin-bottom: 24px; }
        .footer { text-align: center; padding: 32px; color: #9ca3af; font-size: 13px; border-top: 1px solid #e5e7eb; margin-top: 40px; }
        .profile-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; }
        @media (max-width: 768px) { .profile-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body style="margin:0;background:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang SC','Microsoft YaHei',sans-serif;min-height:100vh">
    <header class="portal-header">
        <a href="{% url 'portal:index' %}" class="logo">
            <i class="bi bi-building"></i> 云璟国际酒店
        </a>
        <nav class="portal-nav">
            <a href="{% url 'portal:index' %}">首页</a>
            <a href="{% url 'portal:rooms' %}">客房浏览</a>
            {% if customer %}
            <a href="{% url 'portal:orders' %}">我的订单</a>
            <a href="{% url 'portal:profile' %}">个人中心</a>
            <div class="portal-user">
                <i class="bi bi-person-circle"></i> {{ customer.name }}
                {% if customer.membership %}
                <span style="background:var(--gold-light);color:var(--gold);padding:2px 8px;border-radius:10px;font-size:12px">{{ customer.membership.name }}</span>
                {% endif %}
            </div>
            <a href="{% url 'portal:logout' %}" style="color:#ef4444">退出</a>
            {% else %}
            <a href="{% url 'portal:login' %}">登录</a>
            <a href="{% url 'portal:register' %}" class="btn-book">注册</a>
            {% endif %}
        </nav>
    </header>

    <div class="{% if customer %}portal-content{% else %}portal-content no-auth{% endif %}">
        {% if messages %}
        <div style="max-width:600px;margin:0 auto 20px">
            {% for message in messages %}
            <div style="padding:12px 16px;border-radius:8px;margin-bottom:8px;font-size:14px;{% if message.tags == 'success' %}background:#d1fae5;color:#065f46{% elif message.tags == 'error' %}background:#fee2e2;color:#991b1b{% else %}background:#dbeafe;color:#1e40af{% endif %}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <footer class="footer">
        <p>© 2026 云璟国际酒店 · 北京市朝阳区建国路88号 · 010-88886666</p>
    </footer>
</body>
</html>
'''

os.makedirs(os.path.join(base, "templates", "portal"), exist_ok=True)
with open(os.path.join(base, "templates", "portal", "base.html"), "w", encoding="utf-8") as f:
    f.write(portal_base)

print("Portal base template OK")
