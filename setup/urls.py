from . import views
from django.urls import path

urlpatterns = [
    path('staff/', views.StaffList.as_view(), name='staff' ),
    path('staff/select/', views.select_staff, name='select-staff'),
    
    
]