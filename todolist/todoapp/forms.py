
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'date']
        widgets = {
            'task': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your task...'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
