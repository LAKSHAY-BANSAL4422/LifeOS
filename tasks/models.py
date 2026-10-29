from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Task(models.Model):
    IMPORTANCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    due_date = models.DateField(null=True, blank=True)
    importance = models.CharField(max_length=10, choices=IMPORTANCE_CHOICES, default='medium')
    progress = models.IntegerField(default=0, help_text="Progress from 0 to 100")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def priority_score(self):
        """
        Calculates priority score using exact formula from Report Section 4.9:
        urgency    = 1.0 if days_left <= 0 else max(0, 1 - days_left / 14)
        importance = {'low': 0.33, 'medium': 0.66, 'high': 1.0}
        remaining  = 1 - progress / 100
        priority   = 100 * (0.5*urgency + 0.3*importance + 0.2*remaining)
        Completed tasks are excluded or score 0.
        """
        if self.status == 'done':
            return 0

        today = timezone.now().date()
        if self.due_date:
            days_left = (self.due_date - today).days
        else:
            days_left = 14

        if days_left <= 0:
            urgency = 1.0
        else:
            urgency = max(0.0, 1.0 - (days_left / 14.0))

        importance_map = {
            'low': 0.33,
            'medium': 0.66,
            'high': 1.0,
        }
        importance_val = importance_map.get(self.importance, 0.66)
        remaining = 1.0 - (self.progress / 100.0)

        score = 100.0 * (0.5 * urgency + 0.3 * importance_val + 0.2 * remaining)
        return int(round(score))

    def score_color_class(self):
        score = self.priority_score()
        if score >= 75:
            return 'bg-danger text-white'
        elif score >= 50:
            return 'bg-warning text-dark'
        elif score >= 25:
            return 'bg-success text-white'
        else:
            return 'bg-secondary text-white'
