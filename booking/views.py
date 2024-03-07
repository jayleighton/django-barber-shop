from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView, View
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from setup.models import Info, TradingDays
from home.models import User
from datetime import datetime, timedelta
from .models import Booking

def bookings(request):
    today = datetime(2024,3,5)
    end_date = today + timedelta(days=20)
    print(today)
    # bookings = Booking.objects.filter(booking_start__range=(today.date(), end_date.date()))
    bookings = Booking.objects.filter(booking_start__gte=today.date())
    # bookings = Booking.objects.filter(booking_start__startswith=today.date())
    return render(request, 'booking/booking.html', {
        'data': bookings,
    })