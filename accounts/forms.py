# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 11:04:10 2022

@author: mrdag
"""
from django import forms
from . import models

class SignUpForm(forms.ModelForm):
# create a password field and assign attributes to this field
       password = forms.CharField(widget=forms.PasswordInput(attrs={
              'class': 'field_class form-control',
              'placeholder': 'Enter your password',
       }))
       confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
              'class': 'field_class form-control',
              'placeholder': 'Confirm your password',
       }))
       class Meta():
              model = models.UserAccount
              fields = ['email', 'profile_pic', 'password']

# To validat the data the following clean method is created
       def clean(self):
              cleaned_data = super(SignUpForm, self).clean()
              password = cleaned_data.get('password')
              confirm_password = cleaned_data.get('confirm_password')

              if password != confirm_password:
                     raise forms.ValidationError("Password doesn't match")

# with this init function we initialize the SignUpForm and assign class to the fields
       def __init__(self, *args, **kwargs):
              super(SignUpForm, self).__init__(*args, **kwargs)

              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'field_class form-control'
              self.fields['email'].widget.attrs['placeholder'] = 'Email Address'

