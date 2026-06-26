import os, sys, django
sys.path.insert(0, r"D:\Test_git\hotel_management")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_management.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from customers.models import Customer

# Set passwords for sample customers
customers_data = [
    ("13800138001", "zhang123"),  
    ("13800138002", "li123"),
    ("13800138003", "wang123"),
    ("13800138004", "zhao123"),
]
for phone, pwd in customers_data:
    c = Customer.objects.filter(phone=phone).first()
    if c:
        c.password = make_password(pwd)
        c.save()
        print(f"  {c.name}: {phone} / {pwd}")

print("Customer passwords set!")
