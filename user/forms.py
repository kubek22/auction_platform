from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user.models import User, MAX_USERNAME_LENGTH


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        user.save()
        return user


class LogInForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH)
    password = forms.CharField(widget=forms.PasswordInput)
