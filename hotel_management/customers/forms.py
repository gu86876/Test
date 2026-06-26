from django import forms
from .models import Customer, MembershipLevel

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "gender", "id_card", "phone", "email", "nationality", "birthday", "membership", "preferences", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "gender": forms.Select(attrs={"class":"form-control"}),
            "id_card": forms.TextInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "nationality": forms.TextInput(attrs={"class":"form-control"}),
            "birthday": forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "membership": forms.Select(attrs={"class":"form-control"}),
            "preferences": forms.Textarea(attrs={"class":"form-control","rows":2}),
            "notes": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }

class MembershipForm(forms.ModelForm):
    class Meta:
        model = MembershipLevel
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "code": forms.TextInput(attrs={"class":"form-control"}),
            "discount": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "points_rate": forms.NumberInput(attrs={"class":"form-control","step":"0.1"}),
            "late_checkout_hours": forms.NumberInput(attrs={"class":"form-control"}),
            "min_spending": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "description": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }
