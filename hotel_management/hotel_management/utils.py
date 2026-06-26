import json
from system_config.models import OperationLog

def log_operation(user, action, content, request=None):
    ip = request.META.get('REMOTE_ADDR', '') if request else ''
    OperationLog.objects.create(user=user, action=action, content=content, ip_address=ip)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

def calculate_room_price(room, check_in, check_out):
    from datetime import date
    total = 0
    current = check_in
    while current < check_out:
        price = room.current_price()
        if current.weekday() >= 5:
            if room.room_type.weekend_price > 0:
                price = room.room_type.weekend_price
        total += price
        current = date(current.year, current.month, current.day + 1) if current.day < 28 else current
    return total

def calculate_price(room, check_in, check_out):
    from datetime import date, timedelta
    total = 0
    current = check_in
    while current < check_out:
        price = room.current_price()
        if current.weekday() >= 5 and room.room_type.weekend_price > 0:
            price = room.room_type.weekend_price
        total += price
        current = current + timedelta(days=1)
    return total
