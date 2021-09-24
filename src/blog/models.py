from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
from django.shortcuts import reverse
from PIL import Image
# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image= models.ImageField(upload_to='blog_images' , default='default_book.jpg')
    date = models.DateTimeField(auto_now_add=True)
    spoiled = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog-home")


    def save(self, *args , **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 500  or img.width > 500 :
            img.thumbnail((720,480))
            img.save(self.image.path)
    