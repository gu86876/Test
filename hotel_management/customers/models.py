from django.db import models

class MembershipLevel(models.Model):
    name = models.CharField(verbose_name="等级名称", max_length=50, unique=True)
    code = models.CharField(verbose_name="等级代码", max_length=20, unique=True)
    discount = models.DecimalField(verbose_name="折扣率", max_digits=3, decimal_places=2, default=1.0, help_text="0.85表示85折")
    points_rate = models.DecimalField(verbose_name="积分倍率", max_digits=3, decimal_places=1, default=1.0)
    late_checkout_hours = models.IntegerField(verbose_name="延迟退房(小时)", default=0)
    min_spending = models.DecimalField(verbose_name="最低消费门槛", max_digits=10, decimal_places=2, default=0)
    description = models.TextField(verbose_name="等级说明", blank=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "会员等级"
        verbose_name_plural = "会员等级"

    def __str__(self):
        return self.name

class Customer(models.Model):
    GENDER_CHOICES = [("M", "男"), ("F", "女"), ("O", "其他")]
    name = models.CharField(verbose_name="姓名", max_length=50)
    gender = models.CharField(verbose_name="性别", max_length=1, choices=GENDER_CHOICES, default="M")
    id_card = models.CharField(verbose_name="身份证号", max_length=18, unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="手机号", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=128, default="")
    email = models.EmailField(verbose_name="邮箱", blank=True)
    nationality = models.CharField(verbose_name="国籍", max_length=50, default="中国")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    membership = models.ForeignKey(MembershipLevel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="会员等级")
    points = models.IntegerField(verbose_name="积分", default=0)
    total_spending = models.DecimalField(verbose_name="累计消费", max_digits=12, decimal_places=2, default=0)
    total_stays = models.IntegerField(verbose_name="入住次数", default=0)
    preferences = models.TextField(verbose_name="偏好备注", blank=True)
    is_blacklisted = models.BooleanField(verbose_name="黑名单", default=False)
    is_active = models.BooleanField(verbose_name="账户启用", default=True)
    blacklist_reason = models.TextField(verbose_name="拉黑原因", blank=True)
    notes = models.TextField(verbose_name="备注", blank=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户管理"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"
