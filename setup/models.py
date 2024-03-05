from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

DAYS = ((1, "Monday"), (2, "Tuesday"),(3, "Wednesday"),
        (4, "Thursday"), (5, "Friday"), (6, "Saturday"),
        (7, "Sunday"))


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
    
class TradingDays(models.Model):
    """
    Model to store days and times that store operates
    """
    day = models.IntegerField(choices=DAYS, unique=True)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.open_time} - {self.close_time}"
    
class Service(models.Model):
    """
    Model to store services offered with pricing
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.FloatField(default=0.00)
    is_combo = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.description} {self.price}"

