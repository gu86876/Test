import os
base = r"D:\Test_git\hotel_management"

# 1. Update Customer model - add password field
model_path = os.path.join(base, "customers", "models.py")
with open(model_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add password field after phone
old = "phone = models.CharField(verbose_name=\"手机号\", max_length=20)"
new = "phone = models.CharField(verbose_name=\"手机号\", max_length=20)\n    password = models.CharField(verbose_name=\"密码\", max_length=128, default=\"\")"
content = content.replace(old, new)

# Add is_active field after is_blacklisted
old2 = "is_blacklisted = models.BooleanField(verbose_name=\"黑名单\", default=False)"
new2 = "is_blacklisted = models.BooleanField(verbose_name=\"黑名单\", default=False)\n    is_active = models.BooleanField(verbose_name=\"账户启用\", default=True)"
content = content.replace(old2, new2)

with open(model_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Customer model updated with password field")

# 2. Add __str__ to MembershipLevel if missing
# (already done, skip)

print("Model updates OK")
