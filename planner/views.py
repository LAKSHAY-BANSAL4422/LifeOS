import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date
from planner.models import Event
from planner.forms import EventForm
from academics.models import Assignment, Exam
from tasks.models import Task

@login_required
def calendar_view(request):
    """
    Calendar Month View matching Report Figure: "Calendar and Career tracker"
    """
    user = request.user
    today = timezone.now().date()
    
    # Get requested year and month, default to November 2026 (or current)
    year = int(request.GET.get('year', 2026))
    month = int(request.GET.get('month', 11))

    cal = calendar.Calendar(firstweekday=0) # Monday first
    month_days = cal.monthdatescalendar(year, month)

    events_qs = user.calendar_events.filter(start__year=year, start__month=month)
    assignments_qs = Assignment.objects.filter(subject__user=user, due_date__year=year, due_date__month=month)
    exams_qs = Exam.objects.filter(subject__user=user, date__year=year, date__month=month)
    tasks_qs = user.tasks.filter(due_date__year=year, due_date__month=month, status='pending')

    # Group events by date
    days_data = []
    for week in month_days:
        week_data = []
        for d in week:
            is_current_month = (d.month == month)
            day_events = []
            
            # Planner events
            for ev in events_qs:
                if ev.start.date() == d:
                    day_events.append({
                        'title': ev.title,
                        'type': ev.type,
                        'color': ev.type_color(),
                    })
            # Academic exams
            for ex in exams_qs:
                if ex.date == d:
                    day_events.append({
                        'title': f"{ex.subject.code} {ex.type}",
                        'type': 'exam',
                        'color': '#ef4444',
                    })
            # Assignments
            for a in assignments_qs:
                if a.due_date == d:
                    day_events.append({
                        'title': a.title,
                        'type': 'deadline',
                        'color': '#f59e0b',
                    })

            week_data.append({
                'date': d,
                'day': d.day,
                'is_current_month': is_current_month,
                'is_today': (d == today),
                'events': day_events,
            })
        days_data.append(week_data)

    month_name = calendar.month_name[month]
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render(request, 'planner/calendar.html', {
        'weeks': days_data,
        'year': year,
        'month': month,
        'month_name': month_name,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    })

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.user = request.user
            ev.save()
            messages.success(request, f"Event '{ev.title}' scheduled.")
            return redirect('planner:calendar')
    else:
        form = EventForm()
    return render(request, 'planner/event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    ev = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        ev.delete()
        messages.success(request, "Event removed.")
    return redirect('planner:calendar')
