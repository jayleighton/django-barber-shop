from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_page, name='about'),
    path('', views.home_page, name='home'),
    
]