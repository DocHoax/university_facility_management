from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from accounts.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "department", "role", "first_name", "last_name"]
        widgets = {
            "role": forms.Select(),
            "department": forms.Select(),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")


class ProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "phone_number", "department"]
