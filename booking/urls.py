from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.bookings, name='bookings'),
    path('booking/new/', views.add_booking, name='add-booking'),
    path('bookings/delete/<int:booking_id>', views.delete_booking, name='delete-booking'),
]
