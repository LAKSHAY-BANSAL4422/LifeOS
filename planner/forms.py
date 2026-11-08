from django import forms
from planner.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'type', 'start', 'end', 'description')
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
