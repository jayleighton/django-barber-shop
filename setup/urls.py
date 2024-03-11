from . import views
from django.urls import path

urlpatterns = [
    path('info/', views.shop_info, name='shop-info'),
    path('myprofile/<int:user_id>/', views.show_profile, name='my-profile'),
    path('staff/delete/<int:user_id>/', views.delete_user, name='delete-user'),
    path('trading-days/add/', views.add_trading_day, name='add-trading-days'),
    path('trading-days/delete/<int:day_id>/', views.delete_trading_day, name='delete-trading-day'),
    path('trading-days/edit/<int:day_id>/', views.edit_trading_days, name='edit-trading-days'),
    path('trading-days/', views.TradingDaysList.as_view(), name='show-trading-days'),
    path('services/', views.ServiceList.as_view(), name='services'),
    path('services/add/', views.add_service, name='add-service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete-service'),
    path('service/edit/<int:service_id>/', views.edit_service, name='edit-service'),
    path('staff/', views.StaffList.as_view(), name='staff'),
    path('staff/select/', views.select_staff, name='select-staff'),
    path('staff/edit-staff/<int:staff_id>/', views.edit_staff, name='edit-staff'),
    path('staff/add/<slug:user_id>/', views.add_staff, name='add-staff'),
    
]