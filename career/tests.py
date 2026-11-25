from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import date
from career.models import Application
from planner.models import Event
from django.utils import timezone

class CareerAndPlannerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cp_user', password='password123')
        self.client.login(username='cp_user', password='password123')

    def test_application_lifecycle(self):
        app = Application.objects.create(user=self.user, company='Microsoft', role='SWE Intern', status='applied', applied_date=date.today())
        self.assertEqual(app.status, 'applied')
        self.client.post(f'/career/{app.id}/status/', {'status': 'interview'})
        app.refresh_from_db()
        self.assertEqual(app.status, 'interview')

    def test_event_color_legend(self):
        ev_class = Event.objects.create(user=self.user, title='Lab', type='class', start=timezone.now())
        self.assertEqual(ev_class.type_color(), '#3b82f6') # Blue
        ev_exam = Event.objects.create(user=self.user, title='Midsem', type='exam', start=timezone.now())
        self.assertEqual(ev_exam.type_color(), '#ef4444') # Red
