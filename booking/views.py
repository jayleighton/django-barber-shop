from django.shortcuts import render, redirect, get_object_or_404, reverse
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
from .forms import BookingForm

def bookings(request):
    today = datetime.now()
    context = {}
    if not request.user.is_staff:    
        bookings = Booking.objects.filter(
            booking_start__gte=today.date(),
            customer_id=request.user.id).order_by('booking_start')
        context['data'] = bookings
    elif request.user.is_manager:
        # Change to date + 7
        week_date = today + timedelta(days=15)
        bookings = Booking.objects.filter(
            booking_start__range=(today.date(), week_date.date())).order_by(
                'booking_start')
        context['data'] = bookings
    elif request.user.is_staff:
        bookings = Booking.objects.filter(booking_start__startswith=today.date(),
                                          staff_id=request.user.id).order_by(
                                              'booking_start')
        context['data'] = bookings
    else:
        context['data'] = ''


    return render(request, 'booking/booking.html', context)

@login_required
def delete_booking(request, booking_id):
    queryset = Booking.objects.filter(customer_id=request.user.id)
    booking_to_delete = get_object_or_404(queryset, id=booking_id)
    print(booking_to_delete.id)
    if booking_to_delete.customer_id == request.user or request.user.is_staff:
        print("true")
        booking_to_delete.delete()
        messages.add_message(
            request, messages.SUCCESS,
            'Booking delete successfully'
            )
    else:
        print("false")
        messages.add_message(
            request, messages.ERROR,
            'An error occurred during processing, please call the manager for assistance'
            )
    return HttpResponseRedirect(reverse('bookings'))

def add_booking(request):
    form = BookingForm()
    
    return render(request, 'booking/new_booking.html', {
        'form': form,
    })