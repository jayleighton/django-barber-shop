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
    
class StaffUser(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

   
    
