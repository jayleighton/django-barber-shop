from django import forms
from home.models import User
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
            
