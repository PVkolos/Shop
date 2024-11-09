from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField


class RegisterUserForm(UserCreationForm):
    # username = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # # forms.NumberInput
    # phone = PhoneNumberField(label='Номер телефона', region='RU')
    # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    #
    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password1', 'password2', 'phone')
    username = PhoneNumberField(label='Номер телефона', region='RU')
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # forms.NumberInput
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'last_name', 'email', 'first_name', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

