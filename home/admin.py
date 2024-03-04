from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from .forms import CustomSignUpForm
from .models import User, StaffUser

# Register your models here.
# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(SummernoteModelAdmin):
    list_display = ('username','first_name','last_name', 'email' )
    summernote_fields = ('description',)

