from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.urls.base import reverse
from PIL import Image
from django.utils import timezone
# Create your models here.

class terms(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    number = models.IntegerField(null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("terms")