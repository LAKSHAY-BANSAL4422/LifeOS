from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from career.models import Application
from career.forms import ApplicationForm

@login_required
def applications_list(request):
    """
    Career Tracker matching Report Figure: "Calendar and Career tracker"
    Groups applications by status: Applied, Interview, Offer, Wishlist, Rejected
    """
    user = request.user
    applications = user.career_applications.all()

    applied_list = applications.filter(status='applied')
    interview_list = applications.filter(status='interview')
    offer_list = applications.filter(status='offer')
    wishlist_list = applications.filter(status='wishlist')
    rejected_list = applications.filter(status='rejected')

    return render(request, 'career/applications_list.html', {
        'applied_list': applied_list,
        'interview_list': interview_list,
        'offer_list': offer_list,
        'wishlist_list': wishlist_list,
        'rejected_list': rejected_list,
        'total_count': applications.count(),
    })

@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, f"Application for {app.company} ({app.role}) added.")
            return redirect('career:list')
    else:
        form = ApplicationForm()
    return render(request, 'career/application_form.html', {'form': form})

@login_required
def application_status_update(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            app.status = new_status
            app.save()
            messages.success(request, f"Updated {app.company} status to {app.get_status_display()}.")
    return redirect('career:list')

@login_required
def application_delete(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if request.method == 'POST':
        company = app.company
        app.delete()
        messages.success(request, f"Application for {company} deleted.")
    return redirect('career:list')
