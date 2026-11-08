from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal

class Category(models.Model):
    TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    color = models.CharField(max_length=20, default='#3b82f6')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        sign = '+' if self.type == 'income' else '-'
        return f"{self.note or self.category}: {sign}Rs {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=7, help_text="Format YYYY-MM e.g. 2026-11")

    class Meta:
        unique_together = ('user', 'category', 'month')
        ordering = ['category__name']

    def __str__(self):
        return f"{self.category.name} ({self.month}): Rs {self.monthly_limit}"

    def spent(self):
        total = self.category.transactions.filter(
            user=self.user,
            type='expense',
            date__startswith=self.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        return total

    def remaining(self):
        return self.monthly_limit - self.spent()

    def percentage_spent(self):
        if self.monthly_limit <= 0:
            return 100.0
        return round(float(self.spent() / self.monthly_limit) * 100.0, 1)

    def is_exceeded(self):
        return self.spent() > self.monthly_limit
