from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.bookings, name='bookings')
]
