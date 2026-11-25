from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.demo_data import seed_demo_student

class Command(BaseCommand):
    help = 'Seeds LifeOS with exact sample demo student data from Full Stack Development Lab Report (24B15CS314)'

    def handle(self, *args, **options):
        username = 'demo_student'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': 'demo@jiit.ac.in',
                'first_name': 'Demo',
                'last_name': 'Student',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        user.set_password('password123')
        user.save()

        seed_demo_student(user)
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded demo student '{username}' (password: password123)"))
