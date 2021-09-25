from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.
class testimonial(models.Model):
    content = models.TextField()
    fav = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)


        
    def get_absolute_url(self):
        return reverse("testimonials-detail", kwargs={"id": self.pk})
    
