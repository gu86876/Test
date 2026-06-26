from django.db import models

class RoomType(models.Model):
    name = models.CharField(verbose_name="房型名称", max_length=50, unique=True)
    code = models.CharField(verbose_name="房型代码", max_length=20, unique=True)
    description = models.TextField(verbose_name="描述", blank=True)
    base_price = models.DecimalField(verbose_name="基础价格", max_digits=10, decimal_places=2)
    weekend_price = models.DecimalField(verbose_name="周末价格", max_digits=10, decimal_places=2, default=0)
    holiday_price = models.DecimalField(verbose_name="节假日价格", max_digits=10, decimal_places=2, default=0)
    capacity = models.IntegerField(verbose_name="容纳人数", default=2)
    bed_type = models.CharField(verbose_name="床型", max_length=50, default="大床")
    area = models.CharField(verbose_name="面积", max_length=20, blank=True)
    amenities = models.TextField(verbose_name="设施", blank=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "房型"
        verbose_name_plural = "房型管理"

    def __str__(self):
        return self.name

class Room(models.Model):
    STATUS_CHOICES = [
        ("available", "空闲"),
        ("occupied", "住人"),
        ("reserved", "预定"),
        ("dirty", "脏房"),
        ("maintenance", "维修"),
    ]
    room_number = models.CharField(verbose_name="房间号", max_length=20, unique=True)
    floor = models.IntegerField(verbose_name="楼层", default=1)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="房型")
    status = models.CharField(verbose_name="状态", max_length=20, choices=STATUS_CHOICES, default="available")
    price_override = models.DecimalField(verbose_name="价格覆盖", max_digits=10, decimal_places=2, default=0, help_text="0表示使用房型默认价格")
    notes = models.TextField(verbose_name="备注", blank=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "房间"
        verbose_name_plural = "房间管理"

    def __str__(self):
        return f"{self.room_number} ({self.get_status_display()})"

    def current_price(self):
        if self.price_override > 0:
            return self.price_override
        return self.room_type.base_price

class RoomItem(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="items", verbose_name="房间")
    name = models.CharField(verbose_name="物品名称", max_length=100)
    category = models.CharField(verbose_name="类别", max_length=50, default="消耗品")
    quantity = models.IntegerField(verbose_name="数量", default=1)
    status = models.CharField(verbose_name="状态", max_length=20, choices=[("good","完好"),("damaged","损坏"),("missing","缺失")], default="good")
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "房间物品"
        verbose_name_plural = "房间物品"

    def __str__(self):
        return f"{self.room.room_number} - {self.name}"
