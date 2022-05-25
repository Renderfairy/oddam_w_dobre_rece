from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models.functions import Length
from django.shortcuts import redirect
from django.urls import reverse_lazy

from phonenumber_field.formfields import PhoneNumberField

from . import models


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'name': 'password', 'placeholder': 'Hasło'}))

    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'name': 'password2', 'placeholder': 'Powtórz hasło'}))

    email = forms.CharField(max_length=34, widget=forms.EmailInput(attrs={'name': 'email', 'placeholder': 'Email'}))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'name': 'name', 'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'name': 'surname', 'placeholder': 'Nazwisko'}),
        }

    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        user.is_active = True
        if commit:
            user.save()
            return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=34, widget=forms.EmailInput(attrs={'name': 'email', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'name': 'password', 'placeholder': 'Hasło'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                return redirect(reverse_lazy('donations:register'))
        return super(UserLoginForm, self).clean()


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class AddDonationForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'name': 'phone', 'type': 'phone'}))

    class Meta:
        model = models.Donation
        fields = [
            'quantity',
            'address',
            'city',
            'zip_code',
            'picup_date',
            'picup_time',
            'picup_comment',
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={'name': 'bags', 'step': '1', 'min': '1'}),
            'address': forms.TextInput(attrs={'name': 'address', 'placeholder': 'Dobra 1/3'}),
            'city': forms.TextInput(attrs={'name': 'city'}),
            'zip_code': forms.TextInput(attrs={'name': 'postcode', 'placeholder': '00-000'}),
            'picup_date': DatePickerInput(attrs={'name': 'data'}),
            'picup_time': TimePickerInput(attrs={'name': 'time'}),
            'picup_comment': forms.Textarea(attrs={'name': 'more_info', 'rows': '5'})
        }


# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = models.Category
#         fields = ['name']
