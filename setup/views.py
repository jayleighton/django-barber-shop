from django.shortcuts import render
from django.views import generic
from home.models import User

# Create your views here.
class StaffList(generic.ListView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    template_name = 'setup/staff.html'

def select_staff(request):
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    
    
    return render(request, 'setup/select_staff.html', {
        'data': queryset,
    })
