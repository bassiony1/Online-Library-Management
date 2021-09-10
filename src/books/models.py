from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse
from PIL import Image

# Create your models here.
class book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    cover= models.ImageField(upload_to='book_covers' , default='default.jpg')
    owner = models.ForeignKey(User , on_delete=models.DO_NOTHING , related_name='book_owner')
    borrowed = models.BooleanField(default=False , verbose_name='borrow')
    borrowed_by = models.ForeignKey(User , on_delete=models.SET_NULL , related_name='book_borrowing' , blank=True , null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    ## overrideing The Success_Url  method for The Creation of A book
    def get_absolute_url(self):
        return reverse("all-books")

    ## overriding The save method to modify the cover image before saving it
    def save(self, *args , **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.cover.path)

        if img.height > 500  or img.width > 500 :
            img.thumbnail((500,500))
            img.save(self.cover.path)

    ## overriding the str
    def __str__(self):
        return self.name