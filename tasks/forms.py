from django import forms
from tasks.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'importance', 'progress', 'status')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 5}),
        }
