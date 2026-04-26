from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Department


User = get_user_model()


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "department", "role", "is_active"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "is_active"]
