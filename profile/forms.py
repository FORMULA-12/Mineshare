from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView

from servers.models import *
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django import forms
from django.forms.widgets import ClearableFileInput


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'validate', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'validate',
            'placeholder': 'Пароль',
        }
    ))


class Register(forms.ModelForm):
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'validate', 'placeholder': 'Пароль', 'minlength': '8', 'maxlength': '30'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'validate', 'placeholder': 'Повтор пароля', 'minlength': '8', 'maxlength': '30'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'validate', 'onkeypress': 'return event.which != 32', 'placeholder': 'Логин', 'minlength': '4'}),

            'email': forms.EmailInput(attrs={'class': 'validate', 'placeholder': 'Почта'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class PassEmailForm(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'Почта'})
    )


class PassRecoveryForm(PasswordResetConfirmView):
    new_password1 = forms.CharField(
        label=("Password"),
        max_length=254,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )


class PictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PictureForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ""
        self.fields['image'].label = ""
        self.fields['image'].widget.initial_text = ""
        self.fields['image'].widget.input_text = ""

    class Meta:
        model = Banners
        fields = ('title', 'image')




