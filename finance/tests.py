from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from finance.models import Category, Transaction, Budget

class FinanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='fin_user', password='password123')
        self.client.login(username='fin_user', password='password123')
        self.cat_food = Category.objects.create(user=self.user, name='Food', type='expense')

    def test_monthly_budget_and_exceeded_check(self):
        month = '2026-11'
        b = Budget.objects.create(user=self.user, category=self.cat_food, monthly_limit=Decimal('1500.00'), month=month)

        # Spend 1200
        Transaction.objects.create(user=self.user, category=self.cat_food, amount=Decimal('1200.00'), type='expense', date=date(2026, 11, 10))
        self.assertEqual(b.spent(), Decimal('1200.00'))
        self.assertFalse(b.is_exceeded())

        # Spend another 600 -> 1800 > 1500 (Matches Food in Report Figure!)
        Transaction.objects.create(user=self.user, category=self.cat_food, amount=Decimal('600.00'), type='expense', date=date(2026, 11, 20))
        self.assertEqual(b.spent(), Decimal('1800.00'))
        self.assertTrue(b.is_exceeded())
