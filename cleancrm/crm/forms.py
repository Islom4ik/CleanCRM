from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': "form-control border px-3 py-1", 'id': "login", 'for': 'login', 'autocomplete': 'off'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': "form-control border px-3 py-1", 'id': "password", 'for': 'password'}))

class OperatorCreationForm(UserCreationForm):
    choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password',
        'id': 'pw1',
        'autocomplete': 'off'
    }))

    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password',
        'id': 'pw2',
        'autocomplete': 'off'
    }))

    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter login',
        'id': 'login',
        'autocomplete': 'off'
    }))

    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter first name',
        'id': 'fn'
    }))

    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter last name',
        'id': 'ln'
    }))

    gender = forms.ChoiceField(label='', choices=choices, widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Chose gender',
        'id': 'gender'
    }))

    phone = forms.CharField(label='', max_length=13, validators=[MinLengthValidator(13)], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter phone number',
        'id': 'phone',
        'autocomplete': 'off'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email',
        'id': 'email',
        'autocomplete': 'off'
    }))

    avatar = forms.FileField(label='', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Avatar',
        'id': 'avatar'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')