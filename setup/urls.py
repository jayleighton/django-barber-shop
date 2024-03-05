from . import views
from django.urls import path

urlpatterns = [
    path('info/', views.shop_info, name='shop-info'),
    path('trading-days/add', views.add_trading_day, name='add-trading-days'),
    path('trading-days/edit/<int:day_id>/', views.edit_trading_days, name='edit-trading-days'),
    path('trading-days/', views.show_trading_days, name='show-trading-days'),
    path('staff/', views.StaffList.as_view(), name='staff' ),
    path('staff/select/', views.select_staff, name='select-staff'),
    
    
]