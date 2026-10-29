from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=150)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    start_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def is_done_today(self):
        today = timezone.now().date()
        return self.logs.filter(date=today, completed=True).exists()

    def current_streak(self):
        today = timezone.now().date()
        streak = 0
        check_date = today

        # If today is not done yet, count from yesterday
        if not self.logs.filter(date=today, completed=True).exists():
            check_date = today - timedelta(days=1)

        while True:
            if self.logs.filter(date=check_date, completed=True).exists():
                streak += 1
                check_date = check_date - timedelta(days=1)
            else:
                break
        return streak

    def longest_streak(self):
        logs = list(self.logs.filter(completed=True).values_list('date', flat=True).order_by('date'))
        if not logs:
            return 0
        longest = 1
        current = 1
        for i in range(1, len(logs)):
            if logs[i] - logs[i-1] == timedelta(days=1):
                current += 1
                if current > longest:
                    longest = current
            elif logs[i] == logs[i-1]:
                continue
            else:
                current = 1
        return longest

    def consistency_7d(self):
        today = timezone.now().date()
        start = today - timedelta(days=6)
        done = self.logs.filter(date__gte=start, date__lte=today, completed=True).count()
        return round((done / 7.0) * 100, 1)

    def consistency_30d(self):
        today = timezone.now().date()
        start = today - timedelta(days=29)
        done = self.logs.filter(date__gte=start, date__lte=today, completed=True).count()
        return round((done / 30.0) * 100, 1)


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
