from django import forms

from .models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = (
            'first_name', 'second_name', 'last_name', 'phone', 'address', 'comment'
        )












class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=15)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, max_length=15)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Телефон'
        self.fields['address'].label = 'Адрес'
        self.fields['email'].label = 'E-mail'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} уже существует')
        if len(username) < 5:
            raise forms.ValidationError('Логин состоит хотя бы из 5 символов')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('Пароль состоит хотя бы из 5 символов')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        return email


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone']