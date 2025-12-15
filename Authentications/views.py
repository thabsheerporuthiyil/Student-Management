from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.views.decorators.cache import never_cache


def home(request):
    if request.user.is_authenticated:
        if request.user.role == "admin":
            return redirect("user:admin_dashboard")
        else:
            return redirect("user:student_dashboard")
    return render(request, "home.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("authentication:redirect_dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("authentication:login")
    else:
        form = RegisterForm()

    return render(request, "Authentications/register.html", {"form": form})

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("authentication:redirect_dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("authentication:redirect_dashboard")

    else:
        form = LoginForm(request)

    return render(request, "Authentications/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("authentication:login")

@never_cache
@login_required()
def redirect_dashboard(request):
    user = request.user
    if user.is_superuser or user.role == "admin":
        return redirect("user:admin_dashboard")

    return redirect("user:student_dashboard")