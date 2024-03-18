from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    """
    Extend the User model to include fields required for the app
    """
    description = models.TextField(blank=True)
    image = CloudinaryField('image', default='placeholder')
    is_manager = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username
