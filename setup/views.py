from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth.decorators import login_required
from home.models import User
from .forms import StaffForm

# Create your views here.


class StaffList(generic.ListView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
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
def edit_staff(request, user_id):
    queryset = User.objects.all()
    user = get_object_or_404(queryset, id=user_id)

    # Post method next


    staff_form = StaffForm(instance=user)

    if not request.user.is_staff:
        raise PermissionDenied
    else:
        return render(request, 'setup/add_staff.html', {
            'staff_form': staff_form,
            'users_id': user.id, 
        })