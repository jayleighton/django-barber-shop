from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import User

 
@admin.register(User)
class UserAdmin(SummernoteModelAdmin):
    """
    Class for the User Admin panel
    """
    list_display = ('username','first_name','last_name', 'email' )
    summernote_fields = ('description',)



