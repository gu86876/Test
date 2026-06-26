from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile, Role

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"请输入用户名"}))
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"请输入密码"}))

class UserForm(forms.ModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={"class":"form-control"}), required=False, help_text="留空则不修改密码")
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="角色", widget=forms.Select(attrs={"class":"form-control"}), required=False)

    class Meta:
        model = User
        fields = ["username", "email", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["role", "phone", "id_card", "is_active_staff"]
        widgets = {
            "role": forms.Select(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control"}),
            "id_card": forms.TextInput(attrs={"class":"form-control"}),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "code": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }
