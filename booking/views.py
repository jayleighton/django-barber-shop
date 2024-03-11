from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from setup.models import Info, TradingDays
from home.models import User
from datetime import datetime, timedelta
from .models import Booking
from .forms import BookingForm


class BookingList(LoginRequiredMixin, ListView):
    template_name = 'booking/booking.html'
    context_object_name = 'data'
    model = Booking

    def get_queryset(self, **kwargs):
        queryset = ''
        today = datetime.now()
        if not self.request.user.is_staff:
            queryset = self.model.objects.filter(
                    booking_start__gte=today.date(),
                    customer_id=self.request.user.id).order_by(
                        'booking_start'
                    )
            return queryset
        elif self.request.user.is_manager:
            week_date = today + timedelta(days=7)
            queryset = self.model.objects.filter(
                booking_start__range=(today.date(), week_date.date())).order_by(
                    'booking_start'
                )
            return queryset
        elif self.request.user.is_staff:
            queryset = self.model.objects.filter(
                booking_start__startswith=today.date(),
                staff_id=self.request.user.id).order_by(
                    'booking_start'
                )
            return queryset
        else:
            return None
        
    

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