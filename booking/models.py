from django.db import models
from home.models import User
from setup.models import Service

# Create your models here.
class Booking(models.Model):
    """
    Model for managing booked appointments
    """
    customer_id = models.ForeignKey(User, 
                                    on_delete=models.CASCADE,
                                    related_name='user_id')
    staff_id = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='staff_id')
    service_id = models.ForeignKey(Service,
                                   on_delete=models.CASCADE,
                                   related_name='service_id')
    booking_start = models.DateTimeField()
    booking_end = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    booking_amount = models.FloatField()

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.customer_id} {self.staff_id} {self.service_id} {self.booking_start}'