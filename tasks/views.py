from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tasks.models import Task
from tasks.forms import TaskForm

@login_required
def tasks_list(request):
    """
    Tasks sorted by priority score matching Report Figure: "Tasks sorted by priority score"
    Supports tabs: All, Pending, Done
    """
    user = request.user
    status_filter = request.GET.get('status', 'pending')

    tasks_qs = user.tasks.all()
    if status_filter == 'pending':
        tasks_qs = tasks_qs.filter(status='pending')
    elif status_filter == 'done':
        tasks_qs = tasks_qs.filter(status='done')

    # Convert to list with calculated priority score and sort by priority_score descending
    task_items = []
    for t in tasks_qs:
        score = t.priority_score()
        task_items.append({
            'task': t,
            'score': score,
            'score_class': t.score_color_class(),
        })

    # Sort descending by priority score for pending, or recent for done
    if status_filter != 'done':
        task_items.sort(key=lambda x: x['score'], reverse=True)
    else:
        task_items.sort(key=lambda x: x['task'].updated_at, reverse=True)

    return render(request, 'tasks/tasks_list.html', {
        'task_items': task_items,
        'status_filter': status_filter,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' added.")
            return redirect('tasks:list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated.")
            return redirect('tasks:list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == 'done':
        task.status = 'pending'
        messages.info(request, f"Task '{task.title}' marked as pending.")
    else:
        task.status = 'done'
        task.progress = 100
        messages.success(request, f"Task '{task.title}' completed!")
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'tasks:list'))

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' deleted.")
    return redirect('tasks:list')
