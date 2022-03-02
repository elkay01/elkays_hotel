from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from hotel.models import Booking, Client

class AvailabilityForm(forms.Form):
    ROOM_CATEGORIES=(
        ('ECO', 'ECONOMY'),
        ('FAM', 'FAMILY'),
        ('BUS', 'BUSINESS'),
    )
    room_category = forms.ChoiceField(choices=ROOM_CATEGORIES, required=True)
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])

class BookingForm(forms.Form):
    class Meta:
        models=Booking
        fields=('quantity',)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields=('first_name', 'last_name', 'phone', 'address', 'city','state')