from django.contrib.auth import views as auth
from django.urls import path
from . import views
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth.LoginView.as_view(), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path("password-reset/", auth.PasswordResetView.as_view(), name="password_reset"),
]
