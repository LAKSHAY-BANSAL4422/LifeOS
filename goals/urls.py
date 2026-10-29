from django.urls import path
from goals import views

app_name = 'goals'

urlpatterns = [
    path('', views.goals_list, name='list'),
    path('add/', views.goal_create, name='create'),
    path('<int:pk>/delete/', views.goal_delete, name='delete'),
    path('<int:goal_id>/milestones/add/', views.milestone_create, name='milestone_create'),
    path('milestones/<int:pk>/toggle/', views.milestone_toggle, name='milestone_toggle'),
]
