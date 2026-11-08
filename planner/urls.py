from django.urls import path
from planner import views

app_name = 'planner'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events/add/', views.event_create, name='event_create'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
]
