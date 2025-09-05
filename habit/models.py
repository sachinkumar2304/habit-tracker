from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # har user ke habits
    name = models.CharField(max_length=100)  # habit ka naam
    created_at = models.DateTimeField(auto_now_add=True)  # kab add kiya

    def __str__(self):
        return self.name

# ✅ New Model for Habit Completion Tracking
class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
