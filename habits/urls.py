from django.urls import path
from habits import views

app_name = 'habits'

urlpatterns = [
    path('', views.habits_list, name='list'),
    path('add/', views.habit_create, name='create'),
    path('<int:pk>/toggle/', views.habit_toggle_today, name='toggle_today'),
    path('<int:pk>/delete/', views.habit_delete, name='delete'),
]
