from django import forms
from .models import Booking, CheckInRecord, CheckOutRecord
from rooms.models import Room
from customers.models import Customer

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["customer", "room", "room_type_name", "check_in_date", "check_out_date", "guest_count", "channel", "deposit", "notes"]
        widgets = {
            "customer": forms.Select(attrs={"class":"form-control"}),
            "room": forms.Select(attrs={"class":"form-control"}),
            "room_type_name": forms.TextInput(attrs={"class":"form-control"}),
            "check_in_date": forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "check_out_date": forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "guest_count": forms.NumberInput(attrs={"class":"form-control"}),
            "channel": forms.Select(attrs={"class":"form-control"}),
            "deposit": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "notes": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckInRecord
        fields = ["booking", "customer", "room", "deposit_amount", "id_card_verified", "guest_names", "key_card_no", "notes"]
        widgets = {
            "booking": forms.Select(attrs={"class":"form-control"}),
            "customer": forms.Select(attrs={"class":"form-control"}),
            "room": forms.Select(attrs={"class":"form-control"}),
            "deposit_amount": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "guest_names": forms.Textarea(attrs={"class":"form-control","rows":2}),
            "key_card_no": forms.TextInput(attrs={"class":"form-control"}),
            "notes": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOutRecord
        fields = ["check_in_record", "room_charge", "extra_charges", "penalty", "deposit_used", "payment_method", "invoice_no", "notes"]
        widgets = {
            "check_in_record": forms.Select(attrs={"class":"form-control"}),
            "room_charge": forms.NumberInput(attrs={"class":"form-control","step":"0.01","readonly":"readonly"}),
            "extra_charges": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "penalty": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "deposit_used": forms.NumberInput(attrs={"class":"form-control","step":"0.01"}),
            "payment_method": forms.Select(attrs={"class":"form-control"}),
            "invoice_no": forms.TextInput(attrs={"class":"form-control"}),
            "notes": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }

class CustomerQuickForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "gender", "id_card", "phone", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "gender": forms.Select(attrs={"class":"form-control"}),
            "id_card": forms.TextInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
        }
