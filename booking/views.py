from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from setup.models import TradingDays, Service
from home.models import User
from datetime import datetime, timedelta
from .models import Booking


APPOINTMENT_DURATION = 30


class BookingList(LoginRequiredMixin, ListView):
    """
    View to display list of bookings to the user
    """
    template_name = 'booking/booking.html'
    context_object_name = 'data'
    model = Booking
    paginate_by = 8

    def get_queryset(self, **kwargs):
        queryset = ''
        today = datetime.now()
        if not self.request.user.is_staff:
            # Display list of all bookings for the current user
            queryset = self.model.objects.filter(
                    booking_start__gte=today.date(),
                    customer_id=self.request.user.id).order_by(
                        'booking_start'
                    )
            return queryset
        elif self.request.user.is_manager:
            # Display list of bookings for
            # the next 7 days for all staff members
            week_date = today + timedelta(days=7)
            queryset = self.model.objects.filter(
                booking_start__range=(today.date(),
                                      week_date.date())).order_by(
                                          'booking_start'
                                          )
            return queryset
        elif self.request.user.is_staff:
            # Display list of bookings for the
            # current day and current staff member
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
    """
    View to handle the deletion of an exisitng booking.
    The view receives a booking id and use it to handle
    the deletion of the record
    """
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
            'An error occurred during processing, \
                please call the manager for assistance'
            )
    return HttpResponseRedirect(reverse('bookings'))


class MakeBooking(LoginRequiredMixin, TemplateView):
    """
    View to handle the creation of the form for new bookings.
    The view returns the context based on the
    request and data submitted
    in the form
    """

    template_name = 'booking/make_booking.html'

    def get_context_data(self, **kwargs):
        # Form data
        staff_member_id = self.request.GET.get("staff-member")
        selected_date = self.request.GET.get("booking-date")
        # List of staff members available for booking
        professional = User.objects.filter(
            is_staff=True,
            is_superuser=False,
            is_manager=False).order_by(
                'first_name'
                )
        # List of services available
        services = Service.objects.all().order_by('name')
        context = {}

        if staff_member_id is not None and selected_date is not None:
            # Get available times for staff member and date submitted
            available_times = get_appointment_times(
                staff_member_id, selected_date)
            if len(available_times) == 0:
                available_times = ['None']

            # Populate context for the post values
            context = {
                'available_time': available_times,
                'staff': professional,
                'selected_staff': staff_member_id,
                'service_list': services,
                'date_to_book': selected_date,
            }

            return context

        start_date = datetime.now().date() + timedelta(days=1)
        print(start_date.strftime("%Y-%m-%d"))
        if staff_member_id is not None:
            # Create initial form with staff member already
            # selected from about page
            context = {
                'staff': professional,
                'selected_staff': staff_member_id,
                'date_to_book': start_date.strftime("%Y-%m-%d"),
            }

            return context
        else:
            # Create default initial form
            context = {
                'staff': professional,
                'date_to_book': start_date.strftime("%Y-%m-%d"),
            }

            return context


def get_appointment_times(staff_id, appointment_date):
    """
    Function to calculate available appointment time.
    The function receives the requested staff member and date
    for the calculation.
    The function returns a list object containing available
    appointment times
    If no times are available, the function retuns a list containing 'None'
    """

    # Define appoint date
    sel_year = int(appointment_date.split("-")[0])
    sel_month = int(appointment_date.split("-")[1])
    sel_day = int(appointment_date.split("-")[2])
    appoint_date = datetime(sel_year, sel_month, sel_day)

    # Check if the date is in the past
    if appoint_date.date() < datetime.today().date():
        return []

    # Identify the selected weekday
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
    start_date = datetime(
        sel_year, sel_month,
        sel_day, int(operating_times.open_time.hour),
        int(operating_times.open_time.minute)
        )
    end_date = datetime(
        sel_year, sel_month,
        sel_day, int(operating_times.close_time.hour),
        int(operating_times.close_time.minute)
        )

    # Get bookings for selected date and staff member
    current_bookings = Booking.objects.filter(
        booking_start__startswith=appoint_date.date(),
        staff_id=staff_id
        )
    # Create formatted list of exiting bookings
    current_booking_list = [
        booking.booking_start.replace(tzinfo=None)
        for booking in current_bookings]

    # split day into 30 minutes appointments
    appoint_times = []
    while start_date < end_date:
        if start_date not in current_booking_list:
            # time is available - add to list
            appoint_times.append(start_date)
        # increment time counter
        start_date = start_date + timedelta(
            minutes=APPOINTMENT_DURATION)

    # Create string list of available times
    appoint_calc_times = []
    for n in range(len(appoint_times)):
        ap_start = datetime.time(appoint_times[n])
        ap_end = appoint_times[n] + timedelta(minutes=APPOINTMENT_DURATION)
        ap_end = ap_end.time()
        appoint_calc_times.append(
            f"{ap_start.strftime('%H:%M')} - {ap_end.strftime('%H:%M')}")

    return appoint_calc_times


class SaveBooking(View):
    """
    Model to handle the saving of a new booking from the post form.
    """
    def post(self, *args, **kwargs):
        # Get form values
        selected_date = self.request.POST['booking-date']
        staff_id = self.request.POST['staff-to-book']
        selected_time = self.request.POST['time-select'].split(" - ")
        service_id = self.request.POST['service-select']
        # Create datetime field from submitted values
        appointment_start_date = datetime(
            int(selected_date.split("-")[0]),
            int(selected_date.split("-")[1]),
            int(selected_date.split("-")[2]),
            int(selected_time[0].split(":")[0]),
            int(selected_time[0].split(":")[1])
        )
        # Create the appointment end date and time
        appointment_end_date = appointment_start_date + timedelta(
            minutes=APPOINTMENT_DURATION)
        # Fetch the service and professional from the Model
        selected_service = Service.objects.filter(id=service_id).first()
        staff_member = User.objects.filter(id=staff_id).first()

        # Save the booking to the database
        booking, created = Booking.objects.update_or_create(
            customer_id=self.request.user,
            staff_id=staff_member,
            service_id=selected_service,
            booking_start=appointment_start_date,
            booking_end=appointment_end_date,
            booking_amount=selected_service.price
        )

        # Create success message
        messages.add_message(
                self.request, messages.SUCCESS,
                'Booking completed successfully.'
            )

        return HttpResponseRedirect(reverse('bookings'))
