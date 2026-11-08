from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    TYPE_CHOICES = [
        ('class', 'Class'),
        ('exam', 'Exam'),
        ('deadline', 'Deadline'),
        ('personal', 'Personal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='class')
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return f"{self.title} ({self.get_type_display()}) on {self.start.strftime('%Y-%m-%d')}"

    def type_color(self):
        """
        Color scheme matching Report Figure: Calendar legend:
        Blue: Class, Red: Exam, Orange: Deadline, Green: Personal
        """
        colors = {
            'class': '#3b82f6',     # Blue
            'exam': '#ef4444',      # Red
            'deadline': '#f59e0b',  # Orange
            'personal': '#10b981',  # Green
        }
        return colors.get(self.type, '#3b82f6')
