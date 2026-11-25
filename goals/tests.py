from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import date, timedelta
from goals.models import Goal, Milestone
from habits.models import Habit, HabitLog

class GoalsAndHabitsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='gh_user', password='password123')
        self.client.login(username='gh_user', password='password123')

    def test_goal_milestone_progress(self):
        g = Goal.objects.create(user=self.user, title='Maintain 8.5 CGPA', target_date=date(2027, 5, 20))
        m1 = Milestone.objects.create(goal=g, title='Step 1', completed=True)
        m2 = Milestone.objects.create(goal=g, title='Step 2', completed=False)
        self.assertEqual(g.progress_percentage(), 50)

        # Complete m2 -> 100% and auto-completed status
        m2.completed = True
        m2.save()
        g.refresh_from_db()
        self.assertEqual(g.progress_percentage(), 100)
        self.assertEqual(g.status, 'completed')

    def test_habit_streaks(self):
        today = date.today()
        h = Habit.objects.create(user=self.user, name='Study 2h', start_date=today - timedelta(days=20))
        
        # Log 5 consecutive days
        for i in range(5):
            HabitLog.objects.create(habit=h, date=today - timedelta(days=i), completed=True)

        self.assertTrue(h.is_done_today())
        self.assertEqual(h.current_streak(), 5)
        self.assertEqual(h.longest_streak(), 5)
