from django import forms
from .models import RoomType, Room, RoomItem

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "code": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control","rows":2}),
            "base_price": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "weekend_price": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "holiday_price": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "capacity": forms.NumberInput(attrs={"class":"form-control"}),
            "bed_type": forms.TextInput(attrs={"class":"form-control"}),
            "area": forms.TextInput(attrs={"class":"form-control"}),
            "amenities": forms.Textarea(attrs={"class":"form-control","rows":3}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_number", "floor", "room_type", "status", "price_override", "notes"]
        widgets = {
            "room_number": forms.TextInput(attrs={"class":"form-control"}),
            "floor": forms.NumberInput(attrs={"class":"form-control"}),
            "room_type": forms.Select(attrs={"class":"form-control"}),
            "status": forms.Select(attrs={"class":"form-control"}),
            "price_override": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "notes": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }

class RoomItemForm(forms.ModelForm):
    class Meta:
        model = RoomItem
        fields = "__all__"
        widgets = {
            "room": forms.Select(attrs={"class":"form-control"}),
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "category": forms.TextInput(attrs={"class":"form-control"}),
            "quantity": forms.NumberInput(attrs={"class":"form-control"}),
            "status": forms.Select(attrs={"class":"form-control"}),
        }
