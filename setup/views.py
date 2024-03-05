from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import User, Info, TradingDays
from .forms import StaffForm, ShopInfoForm, TradingDaysForm

# Create your views here.


class StaffList(generic.ListView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False).order_by('date_joined')
    template_name = 'setup/staff.html'


@login_required
def select_staff(request):
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    print(request.user.is_staff)
    
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/select_staff.html', {
            'data': queryset,
        })

@login_required
def shop_info(request):
    queryset = Info.objects.order_by('id').first()
    

    if request.method == 'POST':
        updated_form = ShopInfoForm(data=request.POST, instance=queryset)
        if updated_form.is_valid():
            updated_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Information updated successfully'
            )

    info_form = ShopInfoForm(instance=queryset)

    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/shop_info.html', {
            'info_form': info_form,
        })
    
def show_trading_days(request):
    table_data = TradingDays.objects.order_by('id')
        
    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/trading_days.html', {
            'table_data': table_data,
        })
    
@login_required
def add_trading_day(request):
    if request.method == 'POST':
        form = TradingDaysForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Trading day added successfully'
            )
            return HttpResponseRedirect(reverse('show-trading-days'))
    
    form = TradingDaysForm()

    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/edit-trading-days.html', {
            'form': form,
        })
    



