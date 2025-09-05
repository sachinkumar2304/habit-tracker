from django import forms
from .models import Habit
from django.contrib.auth.forms import AuthenticationForm

# ---------------------------
# Habit Form (existing)
# ---------------------------
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:outline-none text-gray-800',
                'placeholder': 'Enter habit name'
            })
        }

# ---------------------------
# Custom Login Form (for visible input text)
# ---------------------------
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:outline-none text-gray-800',
                'placeholder': field.label
            })
