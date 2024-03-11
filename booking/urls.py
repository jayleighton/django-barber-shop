from django.urls import path
from . import views

urlpatterns = [
    
    path('new/', views.add_booking, name='add-booking'),
    path('delete/<int:booking_id>', views.delete_booking, name='delete-booking'),
    path('', views.BookingList.as_view(), name='bookings'),
]
