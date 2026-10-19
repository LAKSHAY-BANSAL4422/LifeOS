from django.urls import path
from academics import views

app_name = 'academics'

urlpatterns = [
    path('', views.academics_index, name='index'),
    path('subjects/add/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),
    path('attendance/add/', views.attendance_create, name='attendance_create'),
    path('assignments/add/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/toggle/', views.assignment_toggle, name='assignment_toggle'),
    path('exams/add/', views.exam_create, name='exam_create'),
]
