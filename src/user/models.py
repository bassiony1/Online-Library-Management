from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg' , upload_to='profile_pics')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args , **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 500  or img.width > 500 :
            img.thumbnail((720,480))
            img.save(self.image.path)


