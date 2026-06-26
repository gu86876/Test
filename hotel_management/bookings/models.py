from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "待确认"),
        ("confirmed", "已确认"),
        ("checked_in", "已入住"),
        ("checked_out", "已离店"),
        ("cancelled", "已取消"),
        ("no_show", "未到"),
    ]
    CHANNEL_CHOICES = [
        ("online", "在线预订"),
        ("front_desk", "前台预订"),
        ("phone", "电话预订"),
        ("ota", "OTA渠道"),
        ("walk_in", "散客"),
    ]
    order_no = models.CharField(verbose_name="订单号", max_length=32, unique=True)
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, verbose_name="客户")
    room = models.ForeignKey("rooms.Room", on_delete=models.SET_NULL, null=True, verbose_name="房间")
    room_type_name = models.CharField(verbose_name="预订房型", max_length=50, blank=True)
    check_in_date = models.DateField(verbose_name="入住日期")
    check_out_date = models.DateField(verbose_name="离店日期")
    guest_count = models.IntegerField(verbose_name="入住人数", default=1)
    status = models.CharField(verbose_name="订单状态", max_length=20, choices=STATUS_CHOICES, default="pending")
    channel = models.CharField(verbose_name="渠道来源", max_length=20, choices=CHANNEL_CHOICES, default="online")
    total_amount = models.DecimalField(verbose_name="订单总额", max_digits=10, decimal_places=2, default=0)
    deposit = models.DecimalField(verbose_name="订金/押金", max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(verbose_name="备注", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="创建人")
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单管理"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_no} - {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.order_no:
            import uuid, time
            self.order_no = time.strftime("%Y%m%d") + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

class CheckInRecord(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, verbose_name="关联订单")
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, verbose_name="客户")
    room = models.ForeignKey("rooms.Room", on_delete=models.SET_NULL, null=True, verbose_name="入住房间")
    check_in_time = models.DateTimeField(verbose_name="入住时间", auto_now_add=True)
    deposit_amount = models.DecimalField(verbose_name="押金金额", max_digits=10, decimal_places=2, default=0)
    id_card_verified = models.BooleanField(verbose_name="身份已验证", default=False)
    guest_names = models.TextField(verbose_name="同住人", blank=True)
    key_card_no = models.CharField(verbose_name="房卡号", max_length=50, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="办理人")
    notes = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        verbose_name = "入住记录"
        verbose_name_plural = "入住记录"

    def __str__(self):
        return f"{self.booking.order_no} 入住"

class CheckOutRecord(models.Model):
    PAYMENT_CHOICES = [
        ("cash", "现金"),
        ("card", "刷卡"),
        ("wechat", "微信支付"),
        ("alipay", "支付宝"),
        ("credit", "挂账"),
        ("mixed", "混合支付"),
    ]
    check_in_record = models.OneToOneField(CheckInRecord, on_delete=models.CASCADE, verbose_name="关联入住")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="关联订单")
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, verbose_name="客户")
    check_out_time = models.DateTimeField(verbose_name="退房时间", auto_now_add=True)
    room_charge = models.DecimalField(verbose_name="房费", max_digits=10, decimal_places=2, default=0)
    extra_charges = models.DecimalField(verbose_name="其他消费", max_digits=10, decimal_places=2, default=0)
    penalty = models.DecimalField(verbose_name="违约金", max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(verbose_name="消费总额", max_digits=10, decimal_places=2, default=0)
    deposit_used = models.DecimalField(verbose_name="抵扣押金", max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(verbose_name="实收金额", max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(verbose_name="支付方式", max_length=20, choices=PAYMENT_CHOICES, default="cash")
    invoice_no = models.CharField(verbose_name="发票号", max_length=50, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="办理人")
    notes = models.TextField(verbose_name="备注", blank=True)

    class Meta:
        verbose_name = "退房记录"
        verbose_name_plural = "退房记录"

    def __str__(self):
        return f"{self.booking.order_no} 退房"
