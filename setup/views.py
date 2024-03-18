from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import cloudinary.uploader
from home.models import User
from .models import Info,  TradingDays, Service
from .forms import (
    StaffForm, ShopInfoForm, TradingDaysForm, ServiceForm, ProfileForm)


@login_required
def show_profile(request, user_id):
    """
    View to show the current user profile.
    The view receives the current user id to return data from the model
    """
    queryset = User.objects.all()
    user_obj = get_object_or_404(queryset, id=user_id)
    print(user_obj)
    return render(request, 'setup/show-profile.html', {
        'user_data': user_obj
    })


@login_required
def edit_profile(request, user_id):
    """
    View to edit the profile of the current user.
    The view receives the user id of the current user to present data.
    The view uses a POST request to process an update in the Model
    """
    queryset = User.objects.all()
    user_obj = get_object_or_404(queryset, id=user_id)
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=user_obj)
        if form.is_valid():
            record = form.save(commit=False)
            # Upload files to Cloudinary
            if request.FILES:
                cloudinary_response = cloudinary.uploader.upload(
                    request.FILES['image'])
                record.image = cloudinary_response['url']
            record.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'User profile updated successfully'
                                 )
        else:
            # Form is not valid. Show error message
            messages.add_message(request,
                                 messages.ERROR,
                                 'There was an error during processing.'
                                 )

        return HttpResponseRedirect(reverse('my-profile', args=[user_id]))

    # Data for GET request
    user_form = ProfileForm(instance=user_obj)
    return render(request, 'setup/edit-profile.html', {
        'form': user_form,
        'username_value': user_obj.username,
    })


class StaffList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View to display a list of staff members which are employed at the shop
    """
    template_name = 'setup/staff.html'
    context_object_name = 'user_list'
    model = User

    def get_queryset(self, **kwargs):
        """
        Function returns only staff members that are available for bookings
        """
        queryset = self.model.objects.filter(
            is_staff=True, is_superuser=False).order_by(
                'date_joined')
        return queryset

    def test_func(self) -> bool | None:
        """
        Test the request user is a staff member or manager
        """
        return self.request.user.is_staff or self.request.user.is_manager


@login_required
def select_staff(request):
    """
    View to select users that are not staff members for the manager
    to update when creating new staff members
    """

    if not request.user.is_staff:
        raise PermissionDenied
    else:
        queryset = User.objects.filter(is_staff=False, is_superuser=False)
        return render(request, 'setup/select_staff.html', {
            'data': queryset,
        })


@login_required
def add_staff(request, user_id):
    """
    View to update a user as a staff member in the Model.
    The view receives the user id that needs to be displayed or updated.
    """
    if not request.user.is_manager:
        raise PermissionDenied
    else:
        queryset = User.objects.filter(is_staff=False)
        user_obj = get_object_or_404(queryset, id=user_id)
        if request.method == 'POST':
            form = StaffForm(data=request.POST, instance=user_obj)
            if form.is_valid():
                record = form.save(commit=False)
                if request.FILES:
                    cloudinary_response = cloudinary.uploader.upload(
                        request.FILES['image'])
                    record.image = cloudinary_response['url']
                record.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'New staff member updated successfully'
                    )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'There was an error during processing.'
                    )

            return HttpResponseRedirect(reverse('staff'))

        form = StaffForm(instance=user_obj)
        return render(request, 'setup/edit-staff.html', {
            'staff_form': form,
            'mode': 'add',
            'staff_id': user_id,
        })


@login_required
def edit_staff(request, staff_id):
    """
    View to edit and existing staff member.
    Only the manager has access to this view.
    The view receives the staff user id as a parameter to identify the record
    that needs to be updated.
    """
    if not request.user.is_manager:
        raise PermissionDenied
    else:
        queryset = User.objects.filter(is_staff=True)
        staff_obj = get_object_or_404(queryset, id=staff_id)
        if request.method == 'POST':

            form = StaffForm(data=request.POST, instance=staff_obj)

            if form.is_valid():

                record = form.save(commit=False)
                if request.FILES:
                    cloudinary_response = cloudinary.uploader.upload(
                        request.FILES['image'])
                    record.image = cloudinary_response['url']
                record.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'New staff member updated successfully'
                    )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'There was an error during processing.'
                    )
            return HttpResponseRedirect(reverse('staff'))

        form = StaffForm(instance=staff_obj)
        return render(request, 'setup/edit-staff.html', {
            'staff_form': form,
            'mode': 'edit',
            'staff_id': staff_id
        })


@login_required
def shop_info(request):
    """
    View to display and update shop information stored in the database
    """
    queryset = Info.objects.order_by('id').first()

    if request.method == 'POST' and request.user.is_manager:
        updated_form = ShopInfoForm(data=request.POST, instance=queryset)
        if updated_form.is_valid():
            updated_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Information updated successfully'
            )
        return HttpResponseRedirect(reverse('home'))

    info_form = ShopInfoForm(instance=queryset)

    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/shop_info.html', {
            'info_form': info_form,
        })


class TradingDaysList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View to display the trading days and operating times
    stored in the database.
    """
    template_name = 'setup/trading_days.html'
    context_object_name = 'table_data'
    model = TradingDays

    def get_queryset(self, **kwargs):
        """
        Function to return the records from the database
        ordered by the 'day' field
        """
        queryset = self.model.objects.order_by('day')
        return queryset

    def test_func(self) -> bool | None:
        """
        Function to verify that the current user is a
        staff member or the shop manager
        """
        return self.request.user.is_staff or self.request.user.is_manager


@login_required
def add_trading_day(request):
    """
    View to add tradings days to the model
    """
    if request.method == 'POST' and request.user.is_manager:
        form = TradingDaysForm(data=request.POST)
        if form.is_valid():
            print("True")
            result = form.save()
            print(result)
            messages.add_message(
                request, messages.SUCCESS,
                'Trading day added successfully'
            )

        else:
            messages.add_message(
                request, messages.ERROR,
                'Day already exists, please use edit function'
            )
        return HttpResponseRedirect(reverse('show-trading-days'))

    form = TradingDaysForm()

    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/edit-trading-days.html', {
            'form': form,
            'mode': 'add',
        })


@login_required
def edit_trading_days(request, day_id):
    """
    View to edit existing trading days stored in the database
    """
    queryset = TradingDays.objects.all()
    day_to_edit = get_object_or_404(queryset, id=day_id)

    if request.method == 'POST' and request.user.is_manager:
        form = TradingDaysForm(data=request.POST, instance=day_to_edit)
        if form.is_valid():
            print('valid')
            form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Trading day update successfully'
            )
        return HttpResponseRedirect(reverse('show-trading-days'))

    form = TradingDaysForm(instance=day_to_edit)
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/edit-trading-days.html', {
            'form': form,
            'mode': 'edit',
            'day': day_id
        })


@login_required
def delete_trading_day(request, day_id):
    """
    View to delete a trading day record from the database.
    The view receives the id of the record to be deleted.
    """
    if not request.user.is_manager:
        raise PermissionDenied
    else:
        queryset = TradingDays.objects.all()
        day_to_delete = get_object_or_404(queryset, id=day_id)
        day_to_delete.delete()
        messages.add_message(
                    request, messages.SUCCESS,
                    'Trading day deleted successfully'
                )

        return HttpResponseRedirect(reverse('show-trading-days'))


@login_required
def delete_user(request, user_id):
    """
    View to delete users from the user model.
    The view receives the user id as a parameter to identify
    the correct record to delete.
    Access is only provided to the store manager
    """
    if not request.user.is_manager:
        raise PermissionDenied
    else:
        queryset = User.objects.all()
        user_object = get_object_or_404(queryset, id=user_id)
        user_object.delete()
        messages.add_message(
                    request, messages.SUCCESS,
                    'User deleted successfully'
                )
        return HttpResponseRedirect(reverse('staff'))


class ServiceList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View to display the available services
    """
    template_name = 'setup/services.html'
    context_object_name = 'data'
    model = Service

    def test_func(self) -> bool | None:
        """
        Function to verify the request user is a
        staff member or the store manager
        """
        return self.request.user.is_staff or self.request.user.is_manager


@login_required
def add_service(request):
    """
    View to add a new service to the database.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    else:

        if request.method == 'POST' and request.user.is_manager:
            form = ServiceForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(
                        request, messages.SUCCESS,
                        'Service added successfully'
                    )
                return HttpResponseRedirect(reverse('services'))
            else:
                messages.add_message(
                        request, messages.ERROR,
                        'An error occurred during processing. Please try again'
                    )
                return HttpResponseRedirect(reverse('services'))

        form = ServiceForm()

        return render(request, 'setup/edit-service.html', {
            'form': form,
            'mode': 'add',
        })


@login_required
def edit_service(request, service_id):
    """
    View to edit an existing service in the database.
    The view receives the id of the record to be updated.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        queryset = Service.objects.all()
        service_to_edit = get_object_or_404(queryset, id=service_id)
        if request.method == 'POST' and request.user.is_manager:
            form = ServiceForm(data=request.POST, instance=service_to_edit)
            if form.is_valid():
                form.save()
                messages.add_message(
                        request, messages.SUCCESS,
                        'Service updated successfully'
                    )
                return HttpResponseRedirect(reverse('services'))
            else:
                messages.add_message(
                        request, messages.ERROR,
                        'An error occurred during processing. Please try again'
                    )
                return HttpResponseRedirect(reverse('services'))

        form = ServiceForm(instance=service_to_edit)
        return render(request, 'setup/edit-service.html', {
            'form': form,
        })


@login_required
def delete_service(request, service_id):
    """
    View to delete an existing service from the database.
    The view receives the id of the service to be deleted.
    """
    if not request.user.is_manager:
        raise PermissionDenied
    else:
        queryset = Service.objects.all()
        service_to_delete = get_object_or_404(queryset, id=service_id)
        service_to_delete.delete()
        messages.add_message(
            request, messages.SUCCESS,
            'Service deleted successfully'
            )
        return HttpResponseRedirect(reverse('services'))
