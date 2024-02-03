from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserInfo

from django.contrib.auth.models import User

class ContactForm(forms.Form):
    fullname = forms.CharField(label='Name ', 
                               max_length=50, 
                               required=True, 
                               widget= forms.TextInput(attrs={'class':'form-control', 'id':'fullname'}))
    
    subject = forms.CharField(label='Subject ', 
                               max_length=50, 
                               required=True, 
                               widget= forms.TextInput(attrs={'class':'form-control', 'id':'subject'}))
    
    gmail = forms.EmailField(label='Email ', 
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'id':'gmail'}))
    
    phonenumber = forms.IntegerField(label='Phone Number ', 
                                     required=True,
                                     widget=forms.NumberInput(attrs={'class':'form-control', 'id':'pnum'}))
    
    comments = forms.CharField(label='Message ', 
                               max_length=1000, 
                               required=True,
                               widget= forms.Textarea(attrs={'class':'form-control', 'id':'comment'}))

class NewUserForm(forms.Form):
    username = forms.CharField(label='Username', 
                               max_length=50, 
                               required=True, 
                               widget=forms.TextInput(attrs={'class':'form-control', 'id':'username'}))
    password = forms.CharField(label='Password', 
                               max_length=100, 
                               required=True, 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password'}))
    location = forms.CharField(label='Address', 
                               max_length=100, 
                               required=True,
                               widget=forms.TextInput(attrs={'class':'form-control', 'id':'location'}))
    pnumber = forms.CharField(label='Phone Number',
                              max_length=13, 
                              required=True,
                              widget=forms.TextInput(attrs={'class':'form-control', 'id':'pnumber'}))
    first_name = forms.CharField(label='First Name',
                                 max_length=50, 
                                 required=True,
                                 widget=forms.TextInput(attrs={'class':'form-control', 'id':'firstname'}))
    last_name = forms.CharField(label='Last Name',
                                max_length=50, 
                                required=True,
                                widget=forms.TextInput(attrs={'class':'form-control', 'id':'lastname'}))
    email = forms.EmailField(label='Email',
                             required=True,
                             widget=forms.EmailInput(attrs={'class':'form-control','id':'email'}))
    profile = forms.ImageField(required=True, 
                               widget=forms.ClearableFileInput(attrs={'class':'form-control',
                                                                      'type':'file',
                                                                      'id':'profile'}) )

class AddCartForm(forms.Form):
    quantity = forms.IntegerField(initial=1, 
                                  min_value=1, 
                                  max_value=5)
    size = forms.CharField( max_length=10, 
                           required=False)
