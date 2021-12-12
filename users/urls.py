from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("logout/", views.signout, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:username>/<str:key>/",
        views.complete_verification,
        name="verify_email",
    ),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
]
