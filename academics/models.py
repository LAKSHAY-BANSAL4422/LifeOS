from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import math

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30)
    credits = models.DecimalField(max_digits=3, decimal_places=1, default=3.0)
    semester = models.IntegerField(default=5)
    color = models.CharField(max_length=20, default='#3b82f6')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def classes_held(self):
        return self.attendance_logs.count()

    def classes_attended(self):
        return self.attendance_logs.filter(status__in=['present', 'duty_leave']).count()

    def attendance_percentage(self):
        held = self.classes_held()
        if held == 0:
            return 100.0
        attended = self.classes_attended()
        return round((attended / held) * 100.0, 1)

    def attendance_status_info(self):
        """
        Exact formula from Report Section 4.8:
        If P classes attended out of T held and limit is 75%,
        needed = ceil((0.75*T - P) / 0.25)
        """
        held = self.classes_held()
        attended = self.classes_attended()
        if held == 0:
            return {'status': 'Safe', 'needed': 0, 'is_safe': True}

        pct = (attended / held) * 100.0
        if pct >= 75.0:
            return {'status': 'Safe', 'needed': 0, 'is_safe': True}
        else:
            needed = math.ceil((0.75 * held - attended) / 0.25)
            needed = max(1, int(needed))
            return {
                'status': f"Attend next {needed}",
                'needed': needed,
                'is_safe': False
            }


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('duty_leave', 'Duty Leave / Medical'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_logs')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.subject.code} on {self.date}: {self.get_status_display()}"


class Assignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('late', 'Late'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} ({self.subject.code})"


class Exam(models.Model):
    TYPE_CHOICES = [
        ('Mid-sem', 'Mid-Sem Exam'),
        ('End-sem', 'End-Sem Exam'),
        ('Quiz', 'Quiz / Test'),
        ('Practical', 'Practical / Lab Viva'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Mid-sem')
    date = models.DateField()
    maximum_marks = models.DecimalField(max_digits=5, decimal_places=2, default=40.0)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.subject.code} - {self.type} on {self.date}"
