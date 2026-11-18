import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def user_career_directory_path(instance, filename):
    # files will be uploaded to MEDIA_ROOT/career/user_<id>/<filename>
    return f"career/user_{instance.user.id}/{filename}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('wishlist', 'Wishlist'),
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='career_applications')
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, default='')
    document = models.FileField(upload_to=user_career_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_date', '-created_at']

    def __str__(self):
        return f"{self.company} - {self.role} ({self.get_status_display()})"

    @property
    def document_filename(self):
        if self.document:
            return os.path.basename(self.document.name)
        return ""
