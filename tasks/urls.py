from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.tasks_list, name='list'),
    path('add/', views.task_create, name='create'),
    path('<int:pk>/edit/', views.task_edit, name='edit'),
    path('<int:pk>/toggle/', views.task_toggle, name='toggle'),
    path('<int:pk>/delete/', views.task_delete, name='delete'),
]
