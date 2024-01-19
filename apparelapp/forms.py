from django import forms
from apparelapp.models import Cart,Apparel

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
    

class AddCartForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, max_value=5)
    size = forms.CharField( max_length=10, required=False)