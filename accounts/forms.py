from django import forms
from .models import User

class MobileLoginForm(forms.Form):
    mobile = forms.CharField(max_length=15, label="Mobile Number")

class OtpForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mobile', 'role']
