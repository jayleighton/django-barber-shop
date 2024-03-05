from django import forms
from home.models import User
from .models import Info, TradingDays
from django_summernote.widgets import SummernoteWidget
from cloudinary.forms import CloudinaryFileField

class StaffForm(forms.ModelForm):
    image = CloudinaryFileField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_staff', 'description', 'image']
        widgets = {
            'description': SummernoteWidget(),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].options={
                'tags': 'new_image',
            }

class ShopInfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['address1', 'address2','city','country','postal_code','telephone','email']

class TradingDaysForm(forms.ModelForm):
    class Meta:
        model = TradingDays
        fields = ['day', 'open_time', 'close_time']

        widgets = {
            'open_time': forms.TimeInput(attrs={'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'type': 'time'}),
        }
            
