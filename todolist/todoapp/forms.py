
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'date']
        #widgets = {
            #'task': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your task...'}),
            #'date': forms.DateInput(attrs={'type': 'date'}),
       # }
        widgets = {
            'task': forms.TextInput(attrs={'class': 'todo-input'}),
            'date': forms.DateInput(attrs={'class': 'todo-input', 'type':'date'}),
        }
