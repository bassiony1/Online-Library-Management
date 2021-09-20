from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse
from PIL import Image
from django.utils import timezone
# Create your models here.
class book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    cover= models.ImageField(upload_to='book_covers' , default='default_book.jpg')
    owner = models.ForeignKey(User , on_delete=models.DO_NOTHING , related_name='book_owner')
    book_url = models.FileField(upload_to='books',null=True , blank=True)
    borrowed = models.BooleanField(default=False , verbose_name='borrow')
    borrowed_by = models.ForeignKey(User , on_delete=models.SET_NULL , related_name='book_borrowing' , blank=True , null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    borrowed_date = models.DateTimeField(default= None, null=True , blank=True)
    borrowing_duration = models.IntegerField(null=True , blank=True)
    return_date = models.DateTimeField(null=True)
    category =models.ManyToManyField("Category")

    @property
    def return_date(self):
      return self.borrowed_date + timedelta(days=self.borrowing_duration)
    
    @property
    def remaining (self):
        return (self.return_date - self.borrowed_date).days
    
    ## overrideing The Success_Url  method for The Creation of A book
    def get_absolute_url(self):
        return reverse("all-books")

    ## overriding The save method to modify the cover image before saving it
    def save(self, *args , **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.cover.path)

        if img.height > 500  or img.width > 500 :
            img.thumbnail((720,480))
            img.save(self.cover.path)

    ## overriding the str
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
