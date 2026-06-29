from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import Role, UserProfile
from customers.models import MembershipLevel, Customer
from rooms.models import RoomType, Room
from system_config.models import SystemDict, HotelConfig


class Command(BaseCommand):
    help = "初始化种子数据（角色、用户、房型、房间、字典等）"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # ── 角色 ──
        roles = [
            {"name": "管理员", "code": "admin", "description": "系统管理员",
             "can_manage_rooms": True, "can_manage_bookings": True, "can_check_in": True,
             "can_check_out": True, "can_manage_customers": True, "can_view_reports": True,
             "can_manage_system": True, "can_manage_staff": True},
            {"name": "前台经理", "code": "front_manager",
             "can_manage_rooms": True, "can_manage_bookings": True, "can_check_in": True,
             "can_check_out": True, "can_manage_customers": True, "can_view_reports": True},
            {"name": "前台接待", "code": "front_desk",
             "can_manage_bookings": True, "can_check_in": True, "can_check_out": True,
             "can_manage_customers": True},
            {"name": "财务", "code": "finance", "can_view_reports": True},
        ]
        for rd in roles:
            Role.objects.get_or_create(code=rd["code"], defaults=rd)
        self.stdout.write("  Roles created")

        # ── 用户 ──
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser("admin", "admin@hotel.com", "admin123")
            UserProfile.objects.create(user=admin, role=Role.objects.get(code="admin"), phone="13800000000")
        if not User.objects.filter(username="frontdesk").exists():
            fd = User.objects.create_user("frontdesk", password="front123")
            UserProfile.objects.create(user=fd, role=Role.objects.get(code="front_desk"), phone="13900000001")
        self.stdout.write("  Users: admin/admin123, frontdesk/front123")

        # ── 会员等级 ──
        memberships = [
            {"name": "银卡会员", "code": "silver", "discount": 0.95, "points_rate": 1.0, "late_checkout_hours": 1, "min_spending": 1000},
            {"name": "金卡会员", "code": "gold", "discount": 0.88, "points_rate": 1.5, "late_checkout_hours": 2, "min_spending": 5000},
            {"name": "钻石会员", "code": "diamond", "discount": 0.80, "points_rate": 2.0, "late_checkout_hours": 4, "min_spending": 20000},
        ]
        for m in memberships:
            MembershipLevel.objects.get_or_create(code=m["code"], defaults=m)

        # ── 房型 ──
        room_types = [
            {"name": "标准单人房", "code": "STD1", "base_price": 288, "weekend_price": 328, "capacity": 1, "bed_type": "单人床", "area": "20-25m2"},
            {"name": "标准双人房", "code": "STD2", "base_price": 358, "weekend_price": 398, "capacity": 2, "bed_type": "双床", "area": "28-32m2"},
            {"name": "豪华大床房", "code": "DLX", "base_price": 498, "weekend_price": 568, "capacity": 2, "bed_type": "大床", "area": "35-40m2"},
            {"name": "行政套房", "code": "SUITE", "base_price": 888, "weekend_price": 988, "capacity": 4, "bed_type": "大床+沙发床", "area": "55-65m2"},
        ]
        for rt in room_types:
            RoomType.objects.get_or_create(code=rt["code"], defaults=rt)

        # ── 房间 ──
        if Room.objects.count() == 0:
            types = {rt.code: rt for rt in RoomType.objects.all()}
            for floor in range(1, 6):
                max_rooms = 8 if floor <= 3 else 4
                for room_num in range(1, max_rooms + 1):
                    rn = f"{floor}0{room_num}" if room_num < 10 else f"{floor}{room_num}"
                    if floor <= 2:
                        rt = types["STD1"] if room_num <= 4 else types["STD2"]
                    elif floor == 3:
                        rt = types["DLX"]
                    else:
                        rt = types["SUITE"]
                    Room.objects.create(room_number=rn, floor=floor, room_type=rt, status="available")
            self.stdout.write(f"  Generated {Room.objects.count()} rooms")

        # ── 客户 ──
        if Customer.objects.count() == 0:
            silver = MembershipLevel.objects.get(code="silver")
            gold = MembershipLevel.objects.get(code="gold")
            customers = [
                {"name": "张三", "gender": "M", "phone": "13800138001", "membership": gold, "points": 5600, "total_spending": 12800, "total_stays": 12, "password": make_password("zhang123"), "preferences": "喜欢高层房间"},
                {"name": "李四", "gender": "M", "phone": "13800138002", "membership": silver, "points": 1200, "total_spending": 3500, "total_stays": 5, "password": make_password("li123")},
                {"name": "王五", "gender": "F", "phone": "13800138003", "points": 300, "total_spending": 800, "total_stays": 2, "password": make_password("wang123")},
                {"name": "赵六", "gender": "F", "phone": "13800138004", "membership": gold, "points": 8900, "total_spending": 25000, "total_stays": 20, "password": make_password("zhao123"), "preferences": "硬枕头、朝南房间"},
            ]
            for c in customers:
                Customer.objects.create(**c)
            self.stdout.write(f"  Created {Customer.objects.count()} sample customers")

        # ── 字典 ──
        dicts = [
            ("nationality", "中国", "中国", 1), ("nationality", "美国", "美国", 2),
            ("charge_item", "加床费", "加床费", 1), ("charge_item", "洗衣费", "洗衣费", 2),
            ("charge_item", "迷你吧", "迷你吧消费", 3),
            ("bed_type", "单人床", "单人床", 1), ("bed_type", "双床", "双床", 2), ("bed_type", "大床", "大床", 3),
        ]
        for cat, key, val, order in dicts:
            SystemDict.objects.get_or_create(category=cat, key=key, defaults={"value": val, "sort_order": order})

        # ── 酒店配置 ──
        for key, val, desc in [
            ("hotel_name", "云璟国际酒店", "酒店名称"),
            ("hotel_address", "北京市朝阳区建国路88号", "酒店地址"),
            ("hotel_phone", "010-88886666", "酒店电话"),
            ("check_in_time", "14:00", "入住时间"),
            ("check_out_time", "12:00", "退房时间"),
        ]:
            HotelConfig.objects.get_or_create(key=key, defaults={"value": val, "description": desc})

        self.stdout.write(self.style.SUCCESS("Seed data complete!"))
        self.stdout.write("  Staff login:  admin / admin123")
        self.stdout.write("  Staff login:  frontdesk / front123")
        self.stdout.write("  Customer:     13800138001 / zhang123")
