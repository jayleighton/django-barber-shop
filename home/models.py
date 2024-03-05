from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    """
    Extend the User model to include fields required for the app
    """
    description = models.TextField()
    image = CloudinaryField('image', default='placeholder')
    

    def __str__(self):
        return self.username
    

class Info(models.Model):
    """
    Model to store shop information
    """
    address1 = models.CharField(max_length=80, blank=True)
    address2 = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80)
    country = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=80)
    telephone = models.CharField(max_length=80)
    email = models.EmailField()

    def __str__(self):
        return f"{self.address1}, {self.address2}, {self.city}, {self.country}"


   
    
