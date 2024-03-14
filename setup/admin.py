from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin import ModelAdmin
from .models import Info, TradingDays, Service

@admin.register(Info)
class ShopInfo(ModelAdmin):
    list_display = ('address1', 'address2', 'city', 'country', 'telephone', 'email')

@admin.register(TradingDays)
class TradingDaysAdmin(ModelAdmin):
    list_display = ('day', 'open_time', 'close_time')

@admin.register(Service)
class ServiceAdmin(SummernoteModelAdmin):
    list_display = ('name','description','price', 'is_combo', 'created_on', 'updated_on' )
    summernote_fields = ('description',)