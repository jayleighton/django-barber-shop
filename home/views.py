from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect

def home_page(request):
    return render(request, 'home/index.html')
