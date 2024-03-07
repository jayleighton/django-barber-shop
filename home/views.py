from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView, View
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from allauth.account.forms import SignupForm
from django.http import HttpResponseRedirect
from .models import User
from setup.models import Info
from .forms import CustomSignUpForm


def home_page(request):
    queryset = Info.objects.first()
    return render(request, 'home/index.html', {
        'details': queryset,
    })

class CustomSignUpView(SignupForm):
    """
    View for custom signup as a customer or partner
    """
    model = User
    form_class = CustomSignUpForm
    template_name = 'signup.html'

def about_page(request):

    return render(request, 'home/about.html')

    




    