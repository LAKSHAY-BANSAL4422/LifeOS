from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from habits.models import Habit, HabitLog
from habits.forms import HabitForm

@login_required
def habits_list(request):
    user = request.user
    today = timezone.now().date()
    days_14 = [today - timedelta(days=i) for i in range(13, -1, -1)]

    habits = user.habits.all()
    habit_items = []
    for h in habits:
        logs_set = set(h.logs.filter(date__in=days_14, completed=True).values_list('date', flat=True))
        history = [{'date': d, 'completed': d in logs_set} for d in days_14]
        habit_items.append({
            'habit': h,
            'is_done': h.is_done_today(),
            'current_streak': h.current_streak(),
            'longest_streak': h.longest_streak(),
            'consistency_7d': h.consistency_7d(),
            'consistency_30d': h.consistency_30d(),
            'history': history,
        })

    return render(request, 'habits/habits_list.html', {
        'habit_items': habit_items,
        'days_14': days_14,
        'today': today,
    })

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, f"Habit '{habit.name}' created.")
            return redirect('habits:list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form})

@login_required
def habit_toggle_today(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    existing = HabitLog.objects.filter(habit=habit, date=today).first()
    if existing:
        existing.delete()
        messages.info(request, f"Unchecked '{habit.name}' for today.")
    else:
        HabitLog.objects.create(habit=habit, date=today, completed=True)
        messages.success(request, f"Habit '{habit.name}' completed for today! 🔥")
    return redirect(request.META.get('HTTP_REFERER', 'habits:list'))

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        name = habit.name
        habit.delete()
        messages.success(request, f"Habit '{name}' deleted.")
    return redirect('habits:list')
