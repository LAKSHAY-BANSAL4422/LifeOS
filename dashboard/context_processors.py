from django.utils import timezone
from datetime import timedelta

def lifeos_global_context(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    today = timezone.now().date()
    pending_tasks_count = user.tasks.filter(status='pending').count() if hasattr(user, 'tasks') else 0

    return {
        'today': today,
        'global_pending_tasks_count': pending_tasks_count,
    }
