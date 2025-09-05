from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import HabitForm
from .models import Habit, HabitRecord
from datetime import timedelta
import json
from django.views.decorators.cache import never_cache


# ✅ Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")   # already login → dashboard

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


# ✅ Login View
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")   # 🔹 pehle welcome page pe bhejna

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")   # 👈 Ab pehle welcome page
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# ✅ Logout View
@never_cache
def logout_view(request):
    logout(request)
    return redirect("home")   # guest page (welcome)


# ✅ Home (Landing page for guests)
def home(request):
    # Guest ke liye welcome page
    return render(request, "home.html")


# ✅ Dashboard (Welcome page after login)
@login_required
def dashboard(request):
    return render(request, "dashboard.html")   # 👈 Bas welcome page show karega

# ✅ Add Habit
@login_required
def add_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("dashboard")
    else:
        form = HabitForm()
    return render(request, "add_habit.html", {"form": form})


# ✅ Complete Habit
@login_required
def complete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    today = now().date()
    HabitRecord.objects.get_or_create(
        habit=habit, date=today,
        defaults={'completed': True}
    )
    return redirect("dashboard")


# ✅ Progress
@login_required
def progress(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]

    records = []
    for d in dates:
        record = HabitRecord.objects.filter(habit=habit, date=d).first()
        records.append({
            "date": d.strftime("%b %d"),
            "completed": record.completed if record else False
        })

    context = {
        "habit": habit,
        "records_json": json.dumps(records)
    }
    return render(request, "progress.html", context)


# ✅ My Habits (List with history)
@login_required
def my_habits(request):
    habits = Habit.objects.filter(user=request.user)
    last_week = now().date() - timedelta(days=7)
    history = HabitRecord.objects.filter(
        habit__in=habits, date__gte=last_week
    ).order_by("-date")

    today = now().date()
    habit_data = []
    for h in habits:
        completed_today = HabitRecord.objects.filter(
            habit=h, date=today, completed=True
        ).exists()
        habit_data.append({"habit": h, "completed_today": completed_today})

    return render(request, "habits.html", {
        "habit_data": habit_data,
        "history": history
    })
