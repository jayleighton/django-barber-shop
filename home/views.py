from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView, View
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from allauth.account.forms import SignupForm
from django.http import HttpResponseRedirect
from .models import User, StaffUser
from .forms import CustomSignUpForm

def home_page(request):
    return render(request, 'home/index.html')

class CustomSignUpView(SignupForm):
    """
    View for custom signup as a customer or partner
    """
    model = User
    form_class = CustomSignUpForm
    template_name = 'signup.html'

class StaffList(generic.ListView):
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    template_name = 'home/staff.html'

def add_staff(request):
    return render(request, template_name='home/add_staff.html')
    




    