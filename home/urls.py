from . import views
from django.urls import path

urlpatterns = [
    path('staff/', views.StaffList.as_view(), name='staff' ),
    path('', views.home_page, name='home'),
    
]