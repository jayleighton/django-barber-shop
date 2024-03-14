from django.shortcuts import render
from allauth.account.forms import SignupForm
from setup.models import Info, TradingDays
from .models import User
from .forms import CustomSignUpForm


def home_page(request):
    """
    Receives a GET request and renders the index page
    """
    queryset = Info.objects.first()
    days = TradingDays.objects.all().order_by('day')
    
    return render(request, 'home/index.html', {
        'details': queryset,
        'days': days
    })

class CustomSignUpView(SignupForm):
    """
    View for custom signup as a user
    """
    model = User
    form_class = CustomSignUpForm
    template_name = 'signup.html'

def about_page(request):
    """
    View to render the about page to the user
    """
    staff = User.objects.filter(is_staff=True, is_superuser=False).order_by('date_joined')
   
    return render(request, 'home/about.html', {
        'staff_list': staff,
    })
    




    