from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    enrollment_no = models.CharField(max_length=50, blank=True, default='')
    institution = models.CharField(max_length=150, default='Jaypee Institute of Information Technology, Noida')
    department = models.CharField(max_length=150, default='Department of CSE & IT')
    course_name = models.CharField(max_length=100, default='Full Stack Development Lab')
    course_code = models.CharField(max_length=50, default='24B15CS314')
    semester = models.IntegerField(default=5)
    phone = models.CharField(max_length=20, blank=True, default='')
    bio = models.TextField(blank=True, default='B.Tech CSE 3rd Year student at JIIT Noida.')

    def __str__(self):
        return f"{self.user.username} ({self.enrollment_no})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
