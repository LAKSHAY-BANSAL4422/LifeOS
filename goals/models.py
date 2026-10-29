from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Goal(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('career', 'Career'),
        ('personal', 'Personal'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='career')
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['target_date']

    def __str__(self):
        return self.title

    def progress_percentage(self):
        total = self.milestones.count()
        if total == 0:
            return 100 if self.status == 'completed' else 0
        completed = self.milestones.filter(completed=True).count()
        return int(round((completed / total) * 100))

    def is_overdue(self):
        if self.status != 'completed' and self.target_date < timezone.now().date():
            return True
        return False


class Milestone(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date', 'created_at']

    def __str__(self):
        return f"{self.title} ({self.goal.title})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if all milestones are completed
        total = self.goal.milestones.count()
        if total > 0 and self.goal.milestones.filter(completed=True).count() == total:
            self.goal.status = 'completed'
            self.goal.save(update_fields=['status'])
        elif self.goal.status == 'completed' and not self.completed:
            self.goal.status = 'active'
            self.goal.save(update_fields=['status'])
