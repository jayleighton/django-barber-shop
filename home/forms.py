from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import password_validation
from .models import User

class CustomSignUpForm(SignupForm):
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')
    
    

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
    
class add_staff_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','is_staff','description','image',)


        