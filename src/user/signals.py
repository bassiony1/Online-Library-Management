from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def CreateProfile(sender , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
        

post_save.connect(CreateProfile, sender=User)
