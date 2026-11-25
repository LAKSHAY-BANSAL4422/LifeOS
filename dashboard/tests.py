from django.test import TestCase, Client
from django.contrib.auth.models import User
from tasks.models import Task
from academics.models import Subject
from dashboard.demo_data import seed_demo_student

class DashboardAndIsolationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_a = User.objects.create_user(username='student_a', password='Pass4LifeOS!@#')
        self.user_b = User.objects.create_user(username='student_b', password='Pass4LifeOS!@#')

    def test_user_data_isolation(self):
        # User A data
        Task.objects.create(user=self.user_a, title='Private Task A')
        Subject.objects.create(user=self.user_a, name='Secret Subject', code='SEC101')

        # Log in as User B
        self.client.login(username='student_b', password='Pass4LifeOS!@#')
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['pending_tasks_count'], 0)

        # Direct access to User A's task in tasks view should be blocked/not visible
        resp_tasks = self.client.get('/tasks/')
        self.assertEqual(len(resp_tasks.context['task_items']), 0)

    def test_demo_seeder_and_dashboard_metrics(self):
        seed_demo_student(self.user_a)
        self.client.login(username='student_a', password='Pass4LifeOS!@#')
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['pending_tasks_count'], 7)
        self.assertIn(resp.context['avg_attendance'], [80, 81])
        self.assertEqual(resp.context['active_streaks_count'], 4)
        self.assertEqual(resp.context['month_balance'], 3450)
