from django import forms
from goals.models import Goal, Milestone

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title', 'category', 'target_date', 'status')
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ('title', 'due_date', 'completed')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
