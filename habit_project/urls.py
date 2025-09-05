from django.contrib import admin
from django.urls import path, include
from habit import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Root → Welcome page (not dashboard)
    path("", views.home, name="home"),

    # Dashboard (after login)
    path("dashboard/", views.dashboard, name="dashboard"),

    # Habits app urls
    path("habits/", include("habit.urls")),

    # Auth urls
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
