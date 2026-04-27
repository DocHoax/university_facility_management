from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from accounts.forms import LoginForm, ProfileForm, RegistrationForm


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("pages:home")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            messages.success(request, "Registration successful.")
            return redirect("dashboard:home")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            messages.success(request, "Password changed successfully.")
            return redirect("accounts:profile")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})
