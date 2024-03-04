from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    """
    Create custom user
    """
    description = models.TextField()
    image = CloudinaryField('image', default='placeholder')
    

    def __str__(self):
        return self.username
    


   
    
