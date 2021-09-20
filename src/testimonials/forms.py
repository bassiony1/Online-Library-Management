from django import forms
from django.contrib.auth.models import User
from .models import testimonial


class FavForm(forms.ModelForm):
    class Meta:
        model = testimonial
        fields = ['fav']