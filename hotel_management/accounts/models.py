from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(verbose_name="角色名称", max_length=50, unique=True)
    code = models.CharField(verbose_name="角色代码", max_length=50, unique=True)
    description = models.TextField(verbose_name="描述", blank=True)
    can_manage_rooms = models.BooleanField(verbose_name="客房管理", default=False)
    can_manage_bookings = models.BooleanField(verbose_name="预订管理", default=False)
    can_check_in = models.BooleanField(verbose_name="办理入住", default=False)
    can_check_out = models.BooleanField(verbose_name="办理退房", default=False)
    can_manage_customers = models.BooleanField(verbose_name="客户管理", default=False)
    can_view_reports = models.BooleanField(verbose_name="查看报表", default=False)
    can_manage_system = models.BooleanField(verbose_name="系统设置", default=False)
    can_manage_staff = models.BooleanField(verbose_name="员工管理", default=False)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = "角色管理"

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name="角色")
    phone = models.CharField(verbose_name="手机号", max_length=20, blank=True)
    id_card = models.CharField(verbose_name="身份证号", max_length=18, blank=True)
    avatar = models.ImageField(verbose_name="头像", upload_to="avatars/", blank=True)
    is_active_staff = models.BooleanField(verbose_name="在职", default=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案"

    def __str__(self):
        role_name = self.role.name if self.role else "无角色"
        return f"{self.user.username} - {role_name}"
