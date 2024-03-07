from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, ListView, View
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from setup.models import Info, TradingDays
from home.models import User

def bookings(request):
    return render(request, 'booking/booking.html')