from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth.decorators import login_required
from home.models import User
from .forms import StaffForm

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

