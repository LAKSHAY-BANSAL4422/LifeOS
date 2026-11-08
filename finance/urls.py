from django.urls import path
from finance import views

app_name = 'finance'

urlpatterns = [
    path('', views.finance_index, name='index'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('budgets/add/', views.budget_create, name='budget_create'),
    path('categories/add/', views.category_create, name='category_create'),
]
