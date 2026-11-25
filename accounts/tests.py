from django.test import TestCase, Client
from django.contrib.auth.models import User

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_student', email='student@example.test', password='Pass4LifeOS!@#', first_name='Test', last_name='Student')

    def test_registration_and_duplicate_email(self):
        # Successful register with valid strong password
        resp = self.client.post('/register/', {
            'username': 'new_student',
            'first_name': 'New',
            'last_name': 'Student',
            'email': 'new@jiit.ac.in',
            'enrollment_no': '992401030999',
            'semester': 5,
            'password1': 'Pass4LifeOS!@#',
            'password2': 'Pass4LifeOS!@#',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(username='new_student').exists())

        # Duplicate email rejection
        resp_dup = self.client.post('/register/', {
            'username': 'dup_student',
            'first_name': 'Dup',
            'last_name': 'Student',
            'email': 'new@jiit.ac.in',
            'password1': 'Pass4LifeOS!@#',
            'password2': 'Pass4LifeOS!@#',
        })
        self.assertFalse(User.objects.filter(username='dup_student').exists())

    def test_login_and_logout(self):
        # Login
        resp = self.client.post('/login/', {'username': 'test_student', 'password': 'Pass4LifeOS!@#'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['user'].is_authenticated)

        # Logout
        resp_out = self.client.get('/logout/', follow=True)
        self.assertEqual(resp_out.status_code, 200)

    def test_login_required_protection(self):
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp.url)
