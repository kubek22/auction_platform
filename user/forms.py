from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=64)
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
        return user