from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def CreateProfile(sender , **kwargs):
    if kwargs['created']:
        if kwargs['instance'].is_superuser :
            Profile.objects.create(user=kwargs['instance'],is_admin =True)
        else:
            Profile.objects.create(user=kwargs['instance'])

def SaveProfile(sender , **kwargs):
    if kwargs['instance'].is_superuser :
        kwargs['instance'].profile.is_admin=True
        kwargs['instance'].profile.save()
    else :
        kwargs['instance'].profile.save()




post_save.connect(CreateProfile, sender=User)
post_save.connect(SaveProfile, sender=User)
