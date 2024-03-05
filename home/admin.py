from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin import ModelAdmin
from .forms import CustomSignUpForm
from .models import User, Info, TradingDays

# Register your models here.
# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(SummernoteModelAdmin):
    list_display = ('username','first_name','last_name', 'email' )
    summernote_fields = ('description',)

@admin.register(Info)
class ShopInfo(admin.ModelAdmin):
    list_display = ('address1', 'address2', 'city', 'country', 'telephone', 'email')

@admin.register(TradingDays)
class TradingDaysAdmin(admin.ModelAdmin):
    list_display = ('day', 'open_time', 'close_time')

