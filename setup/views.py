from django.shortcuts import render, get_object_or_404, HttpResponse
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


def edit_staff(request, user_id):
    queryset = User.objects.all()
    user = get_object_or_404(queryset, id=user_id)
    print(user.id)

    return render(request, 'setup/add_staff.html', {
        'user': user, 
    })