from . import views
from django.urls import path

urlpatterns = [
    path('staff/', views.StaffList.as_view(), name='staff' ),
    path('staff/edit/<int:user_id>/', views.edit_staff, name='edit-staff'),
    path('staff/select/', views.select_staff, name='select-staff'),
    
    
]