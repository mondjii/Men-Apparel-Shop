from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserInfo

from django.contrib.auth.models import User

class ContactForm(forms.Form):
    Fullname = forms.CharField(label='Name ', 
                               max_length=50, 
                               required=False, 
                               widget= forms.TextInput(attrs={'class':'form-control'}))
    
    gmail = forms.EmailField(label='Email ', 
                             required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    phonenumber = forms.IntegerField(label='Phone Number ', 
                                     required=False,
                                     widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    comments = forms.CharField(label='Message ', 
                               max_length=1000, 
                               required=False,
                               widget= forms.Textarea(attrs={'class':'form-control'}))

class NewUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.PasswordInput)
    location = forms.CharField(label='Address', max_length=100, required=True)
    pnumber = forms.CharField(label='Phone Number',max_length=13, required=True)
    first_name = forms.CharField(label='First Name',max_length=50, required=True)
    last_name = forms.CharField(label='Last Name',max_length=50, required=True)
    email = forms.EmailField(label='Email',required=True)


class AddCartForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=5)
    size = forms.CharField( max_length=10, required=False)