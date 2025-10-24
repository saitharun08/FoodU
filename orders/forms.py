from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['food_item', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }
