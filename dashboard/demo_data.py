"""
LifeOS Demo Data Seeder
Recreates the exact demo state presented in the Project Report:
- Student: Demo Student (Lakshay Bansal / Vanshi Singla / Aashiya Gupta)
- Course: Full Stack Development Lab (24B15CS314) - JIIT Noida
- Supervisor: Ms. Avantika Singh
"""

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import os

from accounts.models import UserProfile
from academics.models import Subject, Attendance, Assignment, Exam
from tasks.models import Task
from goals.models import Goal, Milestone
from habits.models import Habit, HabitLog
from finance.models import Category, Transaction, Budget
from planner.models import Event
from career.models import Application

def seed_demo_student(user):
    # Set display name
    user.first_name = "Demo"
    user.last_name = "Student"
    user.save()

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.enrollment_no = "DEMO-001"
    profile.institution = "Jaypee Institute of Information Technology, Noida"
    profile.department = "Department of CSE & IT"
    profile.course_name = "Full Stack Development Lab"
    profile.course_code = "24B15CS314"
    profile.semester = 5
    profile.bio = "B.Tech CSE 3rd Year 5th Semester student at JIIT Noida. Full Stack Web Development Lab project LifeOS."
    profile.save()

    # Base reference date for demo is November 2026 (from report screenshots)
    ref_year = 2026
    ref_month = 11

    # 1. ACADEMICS (Section 4.8 & Figure: Academics: Attendance)
    # Subjects:
    # Full Stack Development Lab: Held 30, Attended 27 (90%, Safe)
    # Database Management Systems: Held 40, Attended 34 (85%, Safe)
    # Operating Systems: Held 38, Attended 26 (68%, Attend next 10)
    # Computer Networks: Held 36, Attended 24 (67%, Attend next 12)
    # Data Structures: Held 42, Attended 38 (90%, Safe)
    subjects_spec = [
        {"name": "Full Stack Development Lab", "code": "24B15CS314", "credits": Decimal("2.0"), "held": 30, "attended": 27, "color": "#2563eb"},
        {"name": "Database Management Systems", "code": "15B11CI511", "credits": Decimal("4.0"), "held": 40, "attended": 34, "color": "#059669"},
        {"name": "Operating Systems", "code": "15B11CI512", "credits": Decimal("4.0"), "held": 38, "attended": 26, "color": "#dc2626"},
        {"name": "Computer Networks", "code": "15B11CI513", "credits": Decimal("4.0"), "held": 36, "attended": 24, "color": "#d97706"},
        {"name": "Data Structures", "code": "15B11CI311", "credits": Decimal("4.0"), "held": 42, "attended": 38, "color": "#7c3aed"},
    ]

    subject_objs = {}
    for spec in subjects_spec:
        sub, _ = Subject.objects.get_or_create(
            user=user,
            code=spec["code"],
            defaults={
                "name": spec["name"],
                "credits": spec["credits"],
                "semester": 5,
                "color": spec["color"],
            }
        )
        subject_objs[spec["name"]] = sub

        # Generate attendance records to match exact held and attended counts
        if sub.attendance_logs.count() == 0:
            held = spec["held"]
            attended = spec["attended"]
            absent = held - attended
            base_date = date(ref_year, ref_month, 20)
            
            # create attended records
            for i in range(attended):
                d = base_date - timedelta(days=(i * 2 + 1) % 50)
                Attendance.objects.create(subject=sub, date=d, status="present")
            # create absent records
            for i in range(absent):
                d = base_date - timedelta(days=(i * 3 + 2) % 50)
                Attendance.objects.create(subject=sub, date=d, status="absent")

    # Assignments (from Figure: Academics)
    if Assignment.objects.filter(subject__user=user).count() == 0:
        Assignment.objects.create(subject=subject_objs["Database Management Systems"], title="DBMS Assignment 3", due_date=date(ref_year, ref_month, 25), status="pending", max_marks=20)
        Assignment.objects.create(subject=subject_objs["Operating Systems"], title="OS Lab record", due_date=date(ref_year, ref_month, 27), status="pending", max_marks=25)
        Assignment.objects.create(subject=subject_objs["Computer Networks"], title="CN Numericals", due_date=date(ref_year, ref_month, 20), status="submitted", max_marks=20, marks_obtained=18)
        Assignment.objects.create(subject=subject_objs["Data Structures"], title="DSA Problem set", due_date=date(ref_year, ref_month, 18), status="submitted", max_marks=30, marks_obtained=28)

    # Exams (from Figure: Academics)
    if Exam.objects.filter(subject__user=user).count() == 0:
        Exam.objects.create(subject=subject_objs["Database Management Systems"], type="Mid-sem", date=date(2027, 1, 12), maximum_marks=40, marks_obtained=32)
        Exam.objects.create(subject=subject_objs["Operating Systems"], type="Mid-sem", date=date(2027, 1, 14), maximum_marks=40, marks_obtained=29)
        Exam.objects.create(subject=subject_objs["Computer Networks"], type="Mid-sem", date=date(2027, 1, 16), maximum_marks=40, marks_obtained=None)
        Exam.objects.create(subject=subject_objs["Data Structures"], type="Quiz", date=date(ref_year, 12, 2), maximum_marks=20, marks_obtained=18)

    # 2. TASKS (Section 4.9 & Figure: Tasks sorted by priority score)
    # DBMS assignment 3 | 25 Nov | High | 30% | 92
    # Full Stack lab report | 27 Nov | High | 50% | 85
    # Revise OS unit 2 | 30 Nov | Medium | 20% | 61
    # Prepare CN notes | 02 Dec | Medium | 10% | 54
    # Update resume | 10 Dec | High | 40% | 38
    # Clean notes folder | 20 Dec | Low | 0% | 14
    if Task.objects.filter(user=user).count() == 0:
        Task.objects.create(user=user, title="DBMS assignment 3", due_date=date(ref_year, ref_month, 25), importance="high", progress=30, status="pending")
        Task.objects.create(user=user, title="Full Stack lab report", due_date=date(ref_year, ref_month, 27), importance="high", progress=50, status="pending")
        Task.objects.create(user=user, title="Revise OS unit 2", due_date=date(ref_year, ref_month, 30), importance="medium", progress=20, status="pending")
        Task.objects.create(user=user, title="Prepare CN notes", due_date=date(ref_year, 12, 2), importance="medium", progress=10, status="pending")
        Task.objects.create(user=user, title="Update resume", due_date=date(ref_year, 12, 10), importance="high", progress=40, status="pending")
        Task.objects.create(user=user, title="Clean notes folder", due_date=date(ref_year, 12, 20), importance="low", progress=0, status="pending")
        Task.objects.create(user=user, title="DSA LeetCode revision", due_date=date(ref_year, 12, 15), importance="medium", progress=60, status="pending")
        # Completed task
        Task.objects.create(user=user, title="Submit Agile project proposal", due_date=date(ref_year, ref_month, 10), importance="high", progress=100, status="done")

    # 3. GOALS (Section 4.10 & Figure: Dashboard Goal progress)
    # Crack a summer internship: 65%
    # Maintain 8.5 CGPA: 80%
    # Build portfolio website: 40%
    if Goal.objects.filter(user=user).count() == 0:
        g1 = Goal.objects.create(user=user, title="Crack a summer internship", category="career", target_date=date(2027, 6, 30), status="active")
        Milestone.objects.create(goal=g1, title="Master 200 DSA problems", completed=True)
        Milestone.objects.create(goal=g1, title="Build LifeOS fullstack project", completed=True)
        Milestone.objects.create(goal=g1, title="Resume review and mock interviews", completed=False)

        g2 = Goal.objects.create(user=user, title="Maintain 8.5 CGPA", category="academic", target_date=date(2027, 5, 20), status="active")
        Milestone.objects.create(goal=g2, title="Attendance above 80% in all subjects", completed=True)
        Milestone.objects.create(goal=g2, title="Score 30+ in all Mid-sem exams", completed=True)
        Milestone.objects.create(goal=g2, title="Score 35+ in End-sem theory papers", completed=False)

        g3 = Goal.objects.create(user=user, title="Build portfolio website", category="personal", target_date=date(2027, 1, 15), status="active")
        Milestone.objects.create(goal=g3, title="Design responsive layout in Figma", completed=True)
        Milestone.objects.create(goal=g3, title="Deploy on custom domain with GitHub", completed=False)

    # 4. HABITS (Section 4.11 & Figure: Dashboard Habit streaks)
    # Study 2h: 12d
    # Exercise: 5d
    # Reading: 9d
    # Sleep 11pm: 3d
    if Habit.objects.filter(user=user).count() == 0:
        today = timezone.now().date()
        h_specs = [
            ("Study 2h", 12),
            ("Exercise", 5),
            ("Reading", 9),
            ("Sleep 11pm", 3),
        ]
        for name, streak in h_specs:
            h = Habit.objects.create(user=user, name=name, frequency="daily", start_date=today - timedelta(days=streak + 5))
            for day_i in range(streak):
                HabitLog.objects.create(habit=h, date=today - timedelta(days=day_i), completed=True)

    # 5. FINANCE (Section 4.12 & Figure: Finance: November)
    # Income: Rs 8,000
    # Expenses: Rs 4,550
    # Balance: Rs 3,450
    # Categories: Food (1800/1500), Travel (900/1000), Books (600/800), Fun (800/600), Other (450/500)
    cat_food, _ = Category.objects.get_or_create(user=user, name="Food", type="expense", defaults={"color": "#ef4444"})
    cat_travel, _ = Category.objects.get_or_create(user=user, name="Travel", type="expense", defaults={"color": "#3b82f6"})
    cat_books, _ = Category.objects.get_or_create(user=user, name="Books", type="expense", defaults={"color": "#10b981"})
    cat_fun, _ = Category.objects.get_or_create(user=user, name="Fun", type="expense", defaults={"color": "#ef4444"})
    cat_other, _ = Category.objects.get_or_create(user=user, name="Other", type="expense", defaults={"color": "#64748b"})
    cat_income, _ = Category.objects.get_or_create(user=user, name="Allowance & Stipend", type="income", defaults={"color": "#10b981"})

    month_str = f"{ref_year}-{ref_month:02d}"
    if Budget.objects.filter(user=user, month=month_str).count() == 0:
        Budget.objects.create(user=user, category=cat_food, monthly_limit=Decimal("1500.00"), month=month_str)
        Budget.objects.create(user=user, category=cat_travel, monthly_limit=Decimal("1000.00"), month=month_str)
        Budget.objects.create(user=user, category=cat_books, monthly_limit=Decimal("800.00"), month=month_str)
        Budget.objects.create(user=user, category=cat_fun, monthly_limit=Decimal("600.00"), month=month_str)
        Budget.objects.create(user=user, category=cat_other, monthly_limit=Decimal("500.00"), month=month_str)

    if Transaction.objects.filter(user=user, date__startswith=month_str).count() == 0:
        # Incomes adding to 8,000
        Transaction.objects.create(user=user, category=cat_income, amount=Decimal("5000.00"), type="income", date=date(ref_year, ref_month, 19), note="Pocket money")
        Transaction.objects.create(user=user, category=cat_income, amount=Decimal("3000.00"), type="income", date=date(ref_year, ref_month, 5), note="Freelance stipend")
        
        # Expenses adding to 4,550
        # Food: 1800
        Transaction.objects.create(user=user, category=cat_food, amount=Decimal("120.00"), type="expense", date=date(ref_year, ref_month, 20), note="Canteen lunch")
        Transaction.objects.create(user=user, category=cat_food, amount=Decimal("1680.00"), type="expense", date=date(ref_year, ref_month, 10), note="Hostel mess & canteen")
        # Travel: 900
        Transaction.objects.create(user=user, category=cat_travel, amount=Decimal("300.00"), type="expense", date=date(ref_year, ref_month, 18), note="Metro card")
        Transaction.objects.create(user=user, category=cat_travel, amount=Decimal("600.00"), type="expense", date=date(ref_year, ref_month, 8), note="Auto & Metro recharge")
        # Books: 600
        Transaction.objects.create(user=user, category=cat_books, amount=Decimal("600.00"), type="expense", date=date(ref_year, ref_month, 14), note="DBMS & OS reference text")
        # Fun: 800
        Transaction.objects.create(user=user, category=cat_fun, amount=Decimal("800.00"), type="expense", date=date(ref_year, ref_month, 12), note="Weekend movie outing")
        # Other: 450
        Transaction.objects.create(user=user, category=cat_other, amount=Decimal("450.00"), type="expense", date=date(ref_year, ref_month, 16), note="Stationery & printouts")

    # 6. CALENDAR (Section 4.13 & Figure: Calendar and Career tracker)
    # Legend: Blue (Class), Red (Exam), Orange (Deadline), Green (Personal)
    # 3 Nov: Class
    # 7 Nov: Deadline
    # 12 Nov: Personal
    # 18 Nov: Deadline
    # 21 Nov: Class
    # 25 Nov: Exam
    # 28 Nov: Exam
    if Event.objects.filter(user=user).count() == 0:
        Event.objects.create(user=user, title="FSD Lab Lecture", type="class", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 3, 10, 0)))
        Event.objects.create(user=user, title="DSA Assignment Deadline", type="deadline", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 7, 23, 59)))
        Event.objects.create(user=user, title="Doctor Appointment", type="personal", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 12, 16, 0)))
        Event.objects.create(user=user, title="CN Numericals Due", type="deadline", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 18, 23, 59)))
        Event.objects.create(user=user, title="Operating Systems Practical", type="class", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 21, 14, 0)))
        Event.objects.create(user=user, title="DBMS Assignment 3 Due", type="exam", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 25, 9, 30)))
        Event.objects.create(user=user, title="CN Mid-sem exam", type="exam", start=timezone.make_aware(timezone.datetime(ref_year, ref_month, 28, 10, 0)))

    # 7. CAREER TRACKER (Section 4.14 & Figure: Calendar and Career tracker)
    # Applied (2):
    # - Infosys | SDE Intern | resume.pdf
    # - Zoho | Web Dev | resume.pdf
    # Interview (1):
    # - Microsoft | SWE Intern | resume.pdf
    # Offer (1):
    # - Adobe | Product Intern | resume.pdf
    if Application.objects.filter(user=user).count() == 0:
        Application.objects.create(user=user, company="Infosys", role="SDE Intern", status="applied", applied_date=date(ref_year, ref_month, 10), notes="Applied through university on-campus drive.")
        Application.objects.create(user=user, company="Zoho", role="Web Dev", status="applied", applied_date=date(ref_year, ref_month, 14), notes="Applied on careers portal for Chennai/Noida.")
        Application.objects.create(user=user, company="Microsoft", role="SWE Intern", status="interview", applied_date=date(ref_year, ref_month, 2), notes="Cleared Online Assessment (OA). Round 1 Technical scheduled.")
        Application.objects.create(user=user, company="Adobe", role="Product Intern", status="offer", applied_date=date(ref_year, 10, 15), notes="Received 6-month product intern offer letter! 🎉")

    return True
