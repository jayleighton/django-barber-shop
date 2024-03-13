from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from setup.models import Info, TradingDays, Service
from home.models import User
from datetime import datetime, timedelta
from .models import Booking
from .forms import BookingForm

APPOINTMENT_DURATION=30

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

class MakeBooking(LoginRequiredMixin, TemplateView):

    template_name = 'booking/make_booking.html'

    def get_context_data(self, **kwargs):
        staff_member_id = self.request.GET.get("staff-member")
        selected_date = self.request.GET.get("booking-date")
        professional = User.objects.filter(is_staff=True, is_superuser=False, is_manager=False).order_by('first_name')
        services = Service.objects.all().order_by('name')
        context = {}
        if staff_member_id is not None and selected_date is not None:
            available_times = get_appointment_times(staff_member_id, selected_date)
            if len(available_times) == 0:
                available_times = ['None']
            # professional_selected = User.objects.filter(id=staff_member_id)
            context = {
                'available_time': available_times,
                'staff': professional,
                'selected_staff': staff_member_id,
                'service_list': services,
                'date_to_book': selected_date,
            }

            return context

        
        if staff_member_id is not None:
            context = {
                'staff': professional,
                'selected_staff': staff_member_id,
            }
        
            return context
        else:
            context = {
                'staff': professional,
            }

            return context

def get_appointment_times(staff_id, appointment_date):
    # Define appoint date
    sel_year = int(appointment_date.split("-")[0])
    sel_month = int(appointment_date.split("-")[1])
    sel_day = int(appointment_date.split("-")[2])
    appoint_date = datetime(sel_year, sel_month, sel_day)
    day_number = appoint_date.weekday()

    # Get the operating hours from TradingDays
    operating_times = ''
    if day_number >= 0 and day_number <= 4:
        operating_times = TradingDays.objects.filter(day=1).first()
    elif day_number == 5:
        operating_times = TradingDays.objects.filter(day=2).first()
    else:
        operating_times = TradingDays.objects.filter(day=3).first()
    

    # Set the open and closed times for the calculations
    start_date = datetime(sel_year, sel_month, sel_day, int(operating_times.open_time.hour), int(operating_times.open_time.minute))
    end_date = datetime(sel_year, sel_month, sel_day, int(operating_times.close_time.hour), int(operating_times.close_time.minute))
    

    # Get bookings for selected date and staff member
    current_bookings = Booking.objects.filter(booking_start__startswith=appoint_date.date(), staff_id=staff_id)
    
    current_booking_list = [booking.booking_start.replace(tzinfo=None) for booking in current_bookings]
   
   # split day into 30 minutes appointments
    appoint_times = []
    while start_date < end_date:
        if start_date not in current_booking_list:
            # time is available - add to list
            appoint_times.append(start_date)
        # increment time counter
        start_date = start_date + timedelta(minutes=30)

    # Create string list of available times     
    appoint_calc_times = []
    for n in range(len(appoint_times)):
        ap_start = datetime.time(appoint_times[n])
        ap_end = appoint_times[n] + timedelta(minutes=30)
        ap_end = ap_end.time()
        appoint_calc_times.append(f"{ap_start.strftime('%H:%M')} - {ap_end.strftime('%H:%M')}")
        
    
    return appoint_calc_times


class SaveBooking(View):
    def post(self, *args, **kwargs):
        selected_date = self.request.POST['booking-date']
        staff_id = self.request.POST['staff-to-book']
        selected_time = self.request.POST['time-select'].split(" - ")
        service_id = self.request.POST['service-select']
        appointment_start_date = datetime(
            int(selected_date.split("-")[0]),
            int(selected_date.split("-")[1]),
            int(selected_date.split("-")[2]),
            int(selected_time[0].split(":")[0]),
            int(selected_time[0].split(":")[1])
        )
        appointment_end_date = appointment_start_date + timedelta(minutes=APPOINTMENT_DURATION)
        selected_service = Service.objects.filter(id=service_id).first()
        staff_member = User.objects.filter(id=staff_id).first()
        
        booking, created = Booking.objects.update_or_create(
            customer_id = self.request.user,
            staff_id = staff_member,
            service_id = selected_service,
            booking_start = appointment_start_date,
            booking_end = appointment_end_date,
            booking_amount = selected_service.price
        )

        return HttpResponseRedirect(reverse('bookings'))

