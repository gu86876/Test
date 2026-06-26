from django.db import models
from django.contrib.auth.models import User

class SystemDict(models.Model):
    CATEGORY_CHOICES = [
        ("nationality", "国籍"),
        ("charge_item", "收费项目"),
        ("room_facility", "房间设施"),
        ("bed_type", "床型"),
    ]
    category = models.CharField(verbose_name="字典类别", max_length=50, choices=CATEGORY_CHOICES)
    key = models.CharField(verbose_name="键", max_length=100)
    value = models.CharField(verbose_name="值", max_length=200)
    sort_order = models.IntegerField(verbose_name="排序", default=0)
    is_active = models.BooleanField(verbose_name="启用", default=True)
    description = models.TextField(verbose_name="描述", blank=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "系统字典"
        verbose_name_plural = "系统字典"
        unique_together = [("category", "key")]

    def __str__(self):
        return f"[{self.get_category_display()}] {self.key}: {self.value}"

class OperationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="操作人")
    action = models.CharField(verbose_name="操作类型", max_length=50)
    content = models.TextField(verbose_name="操作内容")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="操作时间", auto_now_add=True)

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = "操作日志"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username if self.user else '系统'} - {self.action} - {self.created_at}"

class HotelConfig(models.Model):
    key = models.CharField(verbose_name="配置键", max_length=100, unique=True)
    value = models.TextField(verbose_name="配置值")
    description = models.TextField(verbose_name="描述", blank=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "酒店配置"
        verbose_name_plural = "酒店配置"

    def __str__(self):
        return self.key
