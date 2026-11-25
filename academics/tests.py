from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from academics.models import Subject, Attendance, Assignment, Exam

class AcademicsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='academic_user', password='password123')
        self.client.login(username='academic_user', password='password123')
        self.subject = Subject.objects.create(
            user=self.user,
            name='Operating Systems',
            code='15B11CI512',
            credits=Decimal('4.0'),
            semester=5
        )

    def test_attendance_formula_from_report(self):
        """
        Report Section 4.8 & Figure: Academics: Attendance:
        Operating Systems: Held 38, Attended 26 (68%) -> Attend next 10!
        Formula: ceil((0.75 * held - attended) / 0.25)
        (0.75 * 38 - 26) / 0.25 = 2.5 / 0.25 = 10
        """
        today = date(2026, 11, 20)
        for i in range(26):
            Attendance.objects.create(subject=self.subject, date=today - timedelta(days=i), status='present')
        for i in range(26, 38):
            Attendance.objects.create(subject=self.subject, date=today - timedelta(days=i), status='absent')

        self.assertEqual(self.subject.classes_held(), 38)
        self.assertEqual(self.subject.classes_attended(), 26)
        self.assertEqual(self.subject.attendance_percentage(), 68.4)

        info = self.subject.attendance_status_info()
        self.assertFalse(info['is_safe'])
        self.assertEqual(info['needed'], 10)
        self.assertEqual(info['status'], 'Attend next 10')

    def test_safe_attendance(self):
        """
        Full Stack Development Lab: Held 30, Attended 27 (90%) -> Safe
        """
        sub_fsd = Subject.objects.create(user=self.user, name='Full Stack Lab', code='24B15CS314')
        today = date(2026, 11, 20)
        for i in range(27):
            Attendance.objects.create(subject=sub_fsd, date=today - timedelta(days=i), status='present')
        for i in range(27, 30):
            Attendance.objects.create(subject=sub_fsd, date=today - timedelta(days=i), status='absent')

        self.assertEqual(sub_fsd.attendance_percentage(), 90.0)
        info = sub_fsd.attendance_status_info()
        self.assertTrue(info['is_safe'])
        self.assertEqual(info['status'], 'Safe')

    def test_assignment_toggle(self):
        assign = Assignment.objects.create(
            subject=self.subject,
            title='OS Lab record',
            due_date=date(2026, 11, 27),
            status='pending'
        )
        self.client.get(f'/academics/assignments/{assign.id}/toggle/')
        assign.refresh_from_db()
        self.assertEqual(assign.status, 'submitted')
