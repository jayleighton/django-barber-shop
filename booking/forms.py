from django import forms
from home.models import User
from setup.models import Service, Info, TradingDays
from .models import Booking
import datetime
from django.utils.timezone import now


class BookingForm(forms.ModelForm):
     

    class Meta:
        model = Booking
        fields = ['customer_id', 'staff_id', 'service_id', 'booking_start']

    def save_booking(self, *args, **kwargs):
        data = self.cleaned_data
        if data.get('booking_start') < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past")
        else:
            super(Booking, self).save(*args, **kwargs)
