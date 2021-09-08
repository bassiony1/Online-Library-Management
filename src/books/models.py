from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class book(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    cover= models.ImageField(upload_to='book_covers' , default='default.jpg')
    owner = models.ForeignKey(User , on_delete=models.DO_NOTHING , related_name='book_owner')
    borrowed = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(User , on_delete=models.DO_NOTHING , related_name='book_borrowing' , blank=True , null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name