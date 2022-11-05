from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Staff
        fields = ('username', 'email')


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ['role', 'branch', 'post', 'last_name', 'first_name', 'otchestvo', 'birthday', 'city', 'road', 'house',
                  'flat', 'telephone', 'username', 'email']
        widgets = {
            'role': forms.Select(attrs={'class': 'w-25 form-control'}),
            'branch': forms.Select(attrs={'class': 'w-25 form-control'}),
            'post': forms.Select(attrs={'class': 'w-25 form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'otchestvo': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'w-25 form-control'}),
            'city': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'road': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'house': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'flat': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
            'telephone': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
            'username': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'email': forms.EmailInput(attrs={'class': 'w-25 form-control'}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Staff
        fields = {'username', 'password'}


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Staff
        fields = {'username', 'email', 'password1', 'password2'}


class PactForm(forms.ModelForm):
    class Meta:
        model = Pact
        fields = ['branch', 'type', 'staff', 'client', 'term', 'ssum', 'archive']
        widgets = {
            'branch': forms.Select(attrs={'class': 'w-25 form-control'}),
            'type': forms.Select(attrs={'class': 'w-25 form-control'}),
            'staff': forms.Select(attrs={'class': 'w-25 form-control'}),
            'client': forms.Select(attrs={'class': 'w-25 form-control'}),
            'term': forms.Select(attrs={'class': 'w-25 form-control'}),
            'ssum': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'city', 'road', 'house', 'office', 'telephone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'city': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'road': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'house': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'office': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
            'telephone': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['role', 'branch', 'post', 'last_name', 'first_name', 'otchestvo', 'birthday', 'city', 'road', 'house', 'flat',
                  'telephone', 'username', 'password', 'email']
        widgets = {
            'role': forms.Select(attrs={'class': 'w-25 form-control'}),
            'branch': forms.Select(attrs={'class': 'w-25 form-control'}),
            'post': forms.Select(attrs={'class': 'w-25 form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'otchestvo': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'birthday': DateInput(attrs={'class': 'w-25 form-control'}),
            'city': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'road': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'house': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'flat': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
            'telephone': forms.NumberInput(attrs={'class': 'w-25 form-control'}),
            'username': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'password': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'email': forms.EmailInput(attrs={'class': 'w-25 form-control'}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-25 form-control'}),
            'description': forms.TextInput(attrs={'class': 'w-25 form-control'}),
        }
