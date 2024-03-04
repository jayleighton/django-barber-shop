from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import password_validation
from .models import User

# class CustomSignUpForm(SignupForm):
#     """
#     Custom sign up form for user creation
#     """

#     def __init__(self, *args, **kwargs):
#         super(SignupForm, self).__init__(*args, **kwargs)

#         for fieldname in ['username', 'password1', 'password2']:
#             self.fields[fieldname].help_text = None

#     class Meta(SignupForm.Meta):
#         model = User
#         fields = ('username',
#                   'first_name',
#                   'last_name',
#                   'email',)

class CustomSignUpForm(SignupForm):
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')
    

    def save(self, request):
        user = super(CustomSignUpForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
        