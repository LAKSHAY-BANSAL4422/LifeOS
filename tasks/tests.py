from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

class TasksPriorityScoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='task_user', password='password123')
        self.client.login(username='task_user', password='password123')

    def test_priority_score_calculation(self):
        today = timezone.now().date()
        # Task due tomorrow, high importance, 0 progress
        # days_left = 1 -> urgency = 1 - 1/14 = 13/14 ~ 0.928
        # importance = 1.0
        # remaining = 1.0
        # score = 100 * (0.5 * 0.928 + 0.3 * 1.0 + 0.2 * 1.0) = 100 * (0.464 + 0.3 + 0.2) = 96.4 -> 96
        t = Task.objects.create(
            user=self.user,
            title='High Urgency Task',
            due_date=today + timedelta(days=1),
            importance='high',
            progress=0,
            status='pending'
        )
        self.assertGreaterEqual(t.priority_score(), 90)

        # Completed tasks return score 0
        t.status = 'done'
        self.assertEqual(t.priority_score(), 0)

    def test_task_toggle(self):
        t = Task.objects.create(user=self.user, title='Toggle Task', status='pending', progress=30)
        self.client.get(f'/tasks/{t.id}/toggle/')
        t.refresh_from_db()
        self.assertEqual(t.status, 'done')
        self.assertEqual(t.progress, 100)
