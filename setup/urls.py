from . import views
from django.urls import path

urlpatterns = [
    path('info/', views.shop_info, name='shop-info'),
    path('staff/delete/<int:user_id>', views.delete_user, name='delete-user'),
    path('trading-days/add', views.add_trading_day, name='add-trading-days'),
    path('trading-days/delete/<int:day_id>/', views.delete_trading_day, name='delete-trading-day'),
    path('trading-days/edit/<int:day_id>/', views.edit_trading_days, name='edit-trading-days'),
    path('trading-days/', views.show_trading_days, name='show-trading-days'),
    path('services/', views.show_services, name='services'),
    path('services/add/', views.add_service, name='add-service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete-service'),
    path('service/edit/<int:service_id>/', views.edit_service, name='edit-service'),
    path('staff/', views.StaffList.as_view(), name='staff' ),
    path('staff/select/', views.select_staff, name='select-staff'),
    
    
]