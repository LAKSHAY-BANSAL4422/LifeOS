from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from academics.models import Subject, Attendance, Assignment, Exam
from academics.forms import SubjectForm, AttendanceForm, AssignmentForm, ExamForm

@login_required
def academics_index(request):
    """
    Main Academics page matching Report Figure: "Academics: Attendance"
    - Subject-wise attendance (Held, Attended, Attendance %, Status)
    - Upcoming assignments
    - Examinations and grades
    """
    user = request.user
    subjects = user.subjects.all()

    subject_rows = []
    total_held = 0
    total_attended = 0
    for s in subjects:
        held = s.classes_held()
        attended = s.classes_attended()
        pct = s.attendance_percentage()
        info = s.attendance_status_info()
        total_held += held
        total_attended += attended
        subject_rows.append({
            'subject': s,
            'held': held,
            'attended': attended,
            'percentage': pct,
            'status': info['status'],
            'is_safe': info['is_safe'],
        })

    avg_attendance = round((total_attended / total_held * 100), 1) if total_held > 0 else 100.0

    assignments = Assignment.objects.filter(subject__user=user).select_related('subject')[:10]
    exams = Exam.objects.filter(subject__user=user).select_related('subject')[:10]

    return render(request, 'academics/index.html', {
        'subject_rows': subject_rows,
        'avg_attendance': avg_attendance,
        'assignments': assignments,
        'exams': exams,
    })

@login_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, f"Subject {subject.name} added.")
            return redirect('academics:index')
    else:
        form = SubjectForm()
    return render(request, 'academics/subject_form.html', {'form': form})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject {name} deleted.")
    return redirect('academics:index')

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance record saved.")
            return redirect('academics:index')
    else:
        form = AttendanceForm(request.user)
    return render(request, 'academics/attendance_form.html', {'form': form})

@login_required
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment added.")
            return redirect('academics:index')
    else:
        form = AssignmentForm(request.user)
    return render(request, 'academics/assignment_form.html', {'form': form})

@login_required
def assignment_toggle(request, pk):
    assign = get_object_or_404(Assignment, pk=pk, subject__user=request.user)
    if assign.status == 'submitted':
        assign.status = 'pending'
    else:
        assign.status = 'submitted'
    assign.save()
    messages.success(request, f"Assignment '{assign.title}' marked {assign.get_status_display()}.")
    return redirect('academics:index')

@login_required
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam scheduled.")
            return redirect('academics:index')
    else:
        form = ExamForm(request.user)
    return render(request, 'academics/exam_form.html', {'form': form})
