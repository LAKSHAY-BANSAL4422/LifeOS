from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta, date
from decimal import Decimal
import json

from academics.models import Subject, Assignment, Exam
from tasks.models import Task
from goals.models import Goal
from habits.models import Habit
from finance.models import Transaction, Budget, Category
from planner.models import Event
from dashboard.demo_data import seed_demo_student

@login_required
def dashboard_index(request):
    """
    Main Dashboard matching Report Figure: "Dashboard"
    """
    user = request.user
    today = timezone.now().date()
    month_str = today.strftime('%Y-%m')

    # Top Metric 1: Pending Tasks
    pending_tasks_count = user.tasks.filter(status='pending').count()

    # Top Metric 2: Average Attendance %
    subjects = user.subjects.all()
    total_held = sum(s.classes_held() for s in subjects)
    total_attended = sum(s.classes_attended() for s in subjects)
    avg_attendance = round((total_attended / total_held * 100)) if total_held > 0 else 100

    # Top Metric 3: Active Streaks
    habits = user.habits.all()
    active_streaks_count = sum(1 for h in habits if h.current_streak() > 0)

    # Top Metric 4: Month Balance
    month_txns = user.transactions.filter(date__startswith=month_str)
    month_income = month_txns.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    month_expense = month_txns.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    month_balance = month_income - month_expense

    # Panel 1: Focus now (priority) - top pending tasks ordered by priority score
    pending_tasks = list(user.tasks.filter(status='pending'))
    pending_tasks.sort(key=lambda t: t.priority_score(), reverse=True)
    focus_tasks = []
    for t in pending_tasks[:4]:
        focus_tasks.append({
            'task': t,
            'score': t.priority_score(),
            'score_class': t.score_color_class(),
        })

    # Panel 2: Upcoming deadlines
    # Gather upcoming assignments, exams, and planner deadlines
    upcoming_deadlines = []
    assignments = Assignment.objects.filter(subject__user=user, due_date__gte=today).order_by('due_date')[:3]
    for a in assignments:
        upcoming_deadlines.append({
            'title': a.title,
            'date': a.due_date,
            'type': 'Assignment',
        })
    exams = Exam.objects.filter(subject__user=user, date__gte=today).order_by('date')[:2]
    for ex in exams:
        upcoming_deadlines.append({
            'title': f"{ex.subject.code} {ex.type}",
            'date': ex.date,
            'type': 'Exam',
        })
    events = user.calendar_events.filter(start__date__gte=today, type__in=['exam', 'deadline']).order_by('start')[:2]
    for ev in events:
        upcoming_deadlines.append({
            'title': ev.title,
            'date': ev.start.date(),
            'type': ev.get_type_display(),
        })
    upcoming_deadlines.sort(key=lambda x: x['date'])
    upcoming_deadlines = upcoming_deadlines[:5]

    # Panel 3: Habit streaks
    habit_streak_items = []
    for h in habits[:4]:
        habit_streak_items.append({
            'habit': h,
            'streak': h.current_streak(),
        })

    # Panel 4: Goal progress
    goals = user.goals.filter(status__in=['active', 'completed'])[:4]
    goal_items = []
    for g in goals:
        goal_items.append({
            'goal': g,
            'progress': g.progress_percentage(),
        })

    # Panel 5: Spending this month
    budgets = user.budgets.filter(month=month_str).select_related('category')
    spending_items = []
    for b in budgets[:4]:
        spending_items.append({
            'name': b.category.name,
            'spent': b.spent(),
            'limit': b.monthly_limit,
            'pct': min(100, b.percentage_spent()),
            'color': b.category.color or '#3b82f6',
        })

    return render(request, 'dashboard/index.html', {
        'pending_tasks_count': pending_tasks_count,
        'avg_attendance': avg_attendance,
        'active_streaks_count': active_streaks_count,
        'month_balance': month_balance,
        'focus_tasks': focus_tasks,
        'upcoming_deadlines': upcoming_deadlines,
        'habit_streak_items': habit_streak_items,
        'goal_items': goal_items,
        'spending_items': spending_items,
    })

@login_required
def analytics_view(request):
    """
    Analytics section matching Report Section 4.15
    """
    user = request.user
    today = timezone.now().date()
    month_str = today.strftime('%Y-%m')

    # Subject attendance
    subjects = user.subjects.all()
    sub_names = [s.name[:18] for s in subjects]
    sub_pcts = [s.attendance_percentage() for s in subjects]

    # Spending by category
    category_expenses = (
        user.transactions.filter(type='expense', date__startswith=month_str, category__isnull=False)
        .values('category__name', 'category__color')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    fin_labels = [c['category__name'] for c in category_expenses]
    fin_amounts = [float(c['total']) for c in category_expenses]
    fin_colors = [c['category__color'] or '#3b82f6' for c in category_expenses]

    # Habit consistency (30-day)
    habits = user.habits.all()
    habit_names = [h.name for h in habits]
    habit_consistencies = [h.consistency_30d() for h in habits]

    # Task completion
    total_tasks = user.tasks.count()
    completed_tasks = user.tasks.filter(status='done').count()
    pending_tasks = total_tasks - completed_tasks

    return render(request, 'dashboard/analytics.html', {
        'sub_names_json': json.dumps(sub_names),
        'sub_pcts_json': json.dumps(sub_pcts),
        'fin_labels_json': json.dumps(fin_labels),
        'fin_amounts_json': json.dumps(fin_amounts),
        'fin_colors_json': json.dumps(fin_colors),
        'habit_names_json': json.dumps(habit_names),
        'habit_consistencies_json': json.dumps(habit_consistencies),
        'task_pie_json': json.dumps([completed_tasks, pending_tasks]),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    })

@login_required
def reseed_demo_view(request):
    seed_demo_student(request.user)
    messages.success(request, "LifeOS sample demo student data reloaded successfully!")
    return redirect('dashboard:index')
