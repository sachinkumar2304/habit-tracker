from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # 👇 Dashboard ab sirf Welcome page dikhayega
    path("dashboard/", views.dashboard, name="dashboard"),
    
    path("add-habit/", views.add_habit, name="add_habit"),
    path("complete-habit/<int:habit_id>/", views.complete_habit, name="complete_habit"),
    path("progress/<int:habit_id>/", views.progress, name="progress"),
    
    # 👇 My Habits list alag route pe
    path("habits/", views.my_habits, name="my_habits"),
]
