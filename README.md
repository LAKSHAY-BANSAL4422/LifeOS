# LifeOS — Student Life Management Platform

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1.3-green.svg)](https://www.djangoproject.com/)
[![Course](https://img.shields.io/badge/Course-24B15CS314-orange.svg)]()
[![Institution](https://img.shields.io/badge/JIIT-Noida-blue)]()

> **Full Stack Development Lab (24B15CS314)**  
> **Department of Computer Science & Engineering and Information Technology**  
> **Jaypee Institute of Information Technology (JIIT), Noida**  
> **Under the Supervision of:** Ms. Avantika Singh  
> **Program:** B. Tech. CSE, 3rd Year 5th Semester (2026 - 2027)  

---

## 👥 Student Team Members

| Enrollment No. | Name of Student |
|---|---|
| `992401030189` | **Vanshi Singla** |
| `992401030191` | **Lakshay Bansal** |
| `992401030203` | **Aashiya Gupta** |

---

## 📌 Project Overview

**LifeOS** is a web-based full-stack platform built with Python and Django that centralizes academic, personal, financial, and career tracking for college students into one unified dashboard.

A single dashboard summarises deadlines, productivity, academic indicators, habits, finances, and goal progress, and the application calculates a **Task Priority Score** based on urgency, importance, and remaining progress.

---

## 🛠️ Modules at a Glance (Section 5.2)

| Module | What the user can do | Key Output & Formula |
|---|---|---|
| **Academics** | Manage subjects, attendance, assignments, exams, grades | Attendance % and classes needed formula: `ceil((0.75 * held - attended) / 0.25)` |
| **Tasks** | Add, edit, complete and filter tasks | Priority score: `100 * (0.5 * urgency + 0.3 * importance + 0.2 * remaining)` |
| **Goals** | Define goals and milestones | Progress bar per goal based on completed milestones |
| **Habits** | Log daily habits | Current and longest streaks, 7-day and 30-day consistency % |
| **Finance** | Record income and expenses, set monthly category budgets | Monthly summary (Income, Expenses, Balance) and budget status bars |
| **Calendar** | Add and view events, classes, exams, and deadlines | Month view with color-coded pills (Class, Exam, Deadline, Personal) |
| **Career** | Track applications and upload supporting documents | Status-wise application list (Applied, Interview, Offer, Wishlist, Rejected) |
| **Dashboard** | View all modules together | One-page summary cards, focus now panel, and charts |

---

## 📂 Project Structure (Section 4.2)

```text
lifeos/
|-- manage.py, requirements.txt, README.md
|-- lifeos/            # project settings, urls.py, wsgi.py, asgi.py
|-- accounts/          # registration, login, logout, profile
|-- academics/         # subjects, attendance, assignments, exams, grades
|-- tasks/             # tasks and priority score
|-- goals/             # goals and milestones
|-- habits/            # habits, daily logs, streaks
|-- finance/           # transactions, categories, budgets
|-- planner/           # calendar events and deadlines
|-- career/            # companies, applications, documents
|-- dashboard/         # home dashboard and analytics
|-- templates/         # base.html and per-app templates
|-- static/            # css/, js/
|-- media/             # uploaded career documents
```

---

## ⚡ Setup & Usage (Section 6)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Create the Database Tables
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Seed Sample Demo Student Data
Populates the exact demo dataset described and pictured in the lab report:
```powershell
python manage.py seed_lifeos
```
* **Demo Username:** `demo_student`
* **Demo Password:** `password123`

### Step 4: Start the Server
```powershell
python manage.py runserver
```
Open **http://127.0.0.1:8000/** in your browser.

### Step 5: Run Automated Tests
```powershell
python manage.py test
```
All 15 automated test cases verify user isolation, attendance formulas, priority scores, goal progress, habit streaks, budget exceeded calculations, and calendar event coloring.
