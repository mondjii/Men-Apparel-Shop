from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
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

class BotwearForm(forms.Form):
    quantity = forms.IntegerField(initial=1, 
                                  min_value=1, 
                                  max_value=5)
    size = forms.ChoiceField(required=True,
                             choices=[
                                ('28in', '28 inches'),
                                ('29in', '29 inches'),
                                ('30in', '30 inches'),
                                ('31in', '31 inches'),
                                ('32in', '32 inches'),
                                ('free', '32+ inches (Free Size)')
                            ],
                            widget=forms.RadioSelect)

class TopwearForm(forms.Form):
    quantity = forms.IntegerField(initial=1, 
                                  min_value=1, 
                                  max_value=5)
    size = forms.ChoiceField(required=True,
                             choices=[
                                ('S', 'Small'),
                                ('M', 'Medium'),
                                ('L', 'large'),
                                ('XL', 'X Large'),
                                ('XXL', 'XX Large'),
                                ('XXXL', 'XXX Large')
                            ],
                            widget=forms.RadioSelect)
    
class FootwearForm(forms.Form):
    quantity = forms.IntegerField(initial=1, 
                                  min_value=1, 
                                  max_value=5)
    size = forms.ChoiceField(required=True,
                             choices=[
                                ('8in', '8 inches'),
                                ('8.5in', '8.5 inches'),
                                ('9in', '9 inches'),
                                ('9.5in', '9.5 inches'),
                                ('10in', '10 inches'),
                                ('10.5in', '10.5 inches')
                            ],
                            widget=forms.RadioSelect)