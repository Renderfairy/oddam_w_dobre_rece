from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=20,
                                widget=forms.PasswordInput(attrs={'name': 'password', 'placeholder': 'Hasło'}))
    password2 = forms.CharField(max_length=20,
                                widget=forms.PasswordInput(attrs={'name': 'password2', 'placeholder': 'Powtórz hasło'}))
    email = forms.CharField(max_length=34, widget=forms.EmailInput(attrs={'name': 'email', 'placeholder': 'Email'}))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'name': 'name', 'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'name': 'surname', 'placeholder': 'Nazwisko'}),
        }

    field_order = ['first_name', 'last_name', 'email', 'password1', 'password2']
