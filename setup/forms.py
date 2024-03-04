from django import forms
from home.models import User

class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_staff', 'description', 'image']
