from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('customer_id', 'staff_id', 'service_id', 'booking_start', 'booking_end', 'booking_amount',)

