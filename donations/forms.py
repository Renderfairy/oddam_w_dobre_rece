from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy


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


