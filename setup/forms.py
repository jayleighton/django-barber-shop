from django import forms
from home.models import User
from .models import Info, TradingDays, Service
from django_summernote.widgets import SummernoteWidget
from cloudinary.forms import CloudinaryFileField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Fieldset, Div, HTML, Field

class StaffForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    username = forms.CharField(required=True, disabled=True)
    is_staff = forms.CheckboxInput(),
    required=False
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'description', 'is_staff','image']
        read_only = ['username']
        widgets = {
            'description': SummernoteWidget(),
            'image': CloudinaryFileField(),
            

        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'is_staff': 'Staff Member',
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('is_staff', css_class="form-check-input", wrapper_class="form-check form-switch"),
        )


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
        
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'image']
        widgets = {
            'image': CloudinaryFileField(),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',          
        }
        



class ShopInfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['address1', 'address2','city','country','postal_code','telephone','email']

        labels = {
            'address1': 'Address Line 1',
            'address2': 'Address Line 2',
            'city': 'City',
            'country': 'Country',
            'postal_code': 'Postal Code',
            'telephone': 'Telephone',
            'email': 'Email',
        }


class TradingDaysForm(forms.ModelForm):
    class Meta:
        model = TradingDays
        fields = ['day', 'open_time', 'close_time']

        widgets = {
            'open_time': forms.TimeInput(attrs={'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ServiceForm(forms.ModelForm):
    is_combo = forms.CheckboxInput(),
    required=False
    
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'is_combo']
        widgets = {
            'description': SummernoteWidget(),
        }

        labels = {
            'name': 'Service Name',
            'description': 'Service Description',
            'is_combo': 'Combination Service',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('is_combo', css_class="form-check-input", wrapper_class="form-check form-switch"),
        )

    
        
        
