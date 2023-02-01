from django import forms
from django.contrib.auth.models import User 
from admin_estore.models import UserProfileInfo

class FormUser(forms.ModelForm):
    username = forms.CharField(label = "Username", widget = forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.EmailField(label = "Email", widget = forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    password = forms.CharField(label = "Password", widget = forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(label = "Confirm Password", widget = forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class FormUserProfileInfo(forms.ModelForm):
    portfolio = forms.URLField(label = "Porfolio", widget = forms.TextInput(attrs={
        'class': 'form-control',
    }))
    image = forms.ImageField(label = "Image", widget = forms.FileInput(attrs={
        'class': 'form-control-file',
    }))

    class Meta:
        model = UserProfileInfo
        exclude = ['user']
