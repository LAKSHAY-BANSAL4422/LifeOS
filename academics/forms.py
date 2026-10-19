from django import forms
from academics.models import Subject, Attendance, Assignment, Exam

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'code', 'credits', 'semester', 'color')
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('subject', 'date', 'status')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(user=user)


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('subject', 'title', 'due_date', 'status', 'max_marks', 'marks_obtained')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(user=user)


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('subject', 'type', 'date', 'maximum_marks', 'marks_obtained')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(user=user)
