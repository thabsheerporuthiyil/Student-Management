from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "authentication"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.redirect_dashboard, name="redirect_dashboard"),

    # Password Reset
    path("password-reset/", auth_views.PasswordResetView.as_view(
            template_name="Authentications/password_reset.html",
            email_template_name="Authentications/password_reset_email.txt",
            subject_template_name="Authentications/password_reset_subject.txt",
            success_url=reverse_lazy("authentication:password_reset_done"),
        ),
        name="password_reset",
    ),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
            template_name="Authentications/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
            template_name="Authentications/password_reset_confirm.html",
            success_url=reverse_lazy("authentication:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
            template_name="Authentications/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
