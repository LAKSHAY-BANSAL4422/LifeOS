from django.urls import path
from career import views

app_name = 'career'

urlpatterns = [
    path('', views.applications_list, name='list'),
    path('add/', views.application_create, name='create'),
    path('<int:pk>/status/', views.application_status_update, name='status_update'),
    path('<int:pk>/delete/', views.application_delete, name='delete'),
]
