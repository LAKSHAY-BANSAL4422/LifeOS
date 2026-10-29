from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from goals.models import Goal, Milestone
from goals.forms import GoalForm, MilestoneForm

@login_required
def goals_list(request):
    user = request.user
    goals = user.goals.prefetch_related('milestones').all()
    goal_cards = []
    for g in goals:
        goal_cards.append({
            'goal': g,
            'progress': g.progress_percentage(),
            'is_overdue': g.is_overdue(),
            'milestones': g.milestones.all(),
        })

    return render(request, 'goals/goals_list.html', {
        'goal_cards': goal_cards,
    })

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f"Goal '{goal.title}' added.")
            return redirect('goals:list')
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        title = goal.title
        goal.delete()
        messages.success(request, f"Goal '{title}' deleted.")
    return redirect('goals:list')

@login_required
def milestone_create(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.goal = goal
            milestone.save()
            messages.success(request, f"Milestone added to '{goal.title}'.")
            return redirect('goals:list')
    else:
        form = MilestoneForm()
    return render(request, 'goals/milestone_form.html', {'form': form, 'goal': goal})

@login_required
def milestone_toggle(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk, goal__user=request.user)
    milestone.completed = not milestone.completed
    milestone.save()
    messages.success(request, f"Milestone '{milestone.title}' updated.")
    return redirect('goals:list')
