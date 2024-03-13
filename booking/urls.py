from django.urls import path
from . import views

urlpatterns = [
    
    path('new/', views.add_booking, name='add-booking'),
    path('add/', views.MakeBooking.as_view(), name='new-booking'),
    path('delete/<int:booking_id>', views.delete_booking, name='delete-booking'),
    path('save/', views.SaveBooking.as_view(), name='save-booking'),
    path('', views.BookingList.as_view(), name='bookings'),
]
