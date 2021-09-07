from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Profile



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_admin']
class ProfileUpdateForm(forms.ModelForm):
    class Meta :
        model = Profile
        fields = ['image']
