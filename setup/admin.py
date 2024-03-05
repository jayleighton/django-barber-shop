from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin import ModelAdmin
from .models import Info, TradingDays

@admin.register(Info)
class ShopInfo(admin.ModelAdmin):
    list_display = ('address1', 'address2', 'city', 'country', 'telephone', 'email')

@admin.register(TradingDays)
class TradingDaysAdmin(admin.ModelAdmin):
    list_display = ('day', 'open_time', 'close_time')