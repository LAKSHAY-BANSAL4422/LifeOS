from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from finance.models import Category, Transaction, Budget
from finance.forms import TransactionForm, BudgetForm, CategoryForm

@login_required
def finance_index(request):
    """
    Finance page matching Report Figure: "Finance: November"
    - Monthly summary: Income, Expenses, Balance
    - Spending by category bars
    - Budget status list with limits and progress bars
    - Recent transactions list
    """
    user = request.user
    today = timezone.now().date()
    month_filter = request.GET.get('month', today.strftime('%Y-%m'))

    # Calculate month totals
    month_txns = user.transactions.filter(date__startswith=month_filter)
    income_total = month_txns.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    expense_total = month_txns.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    balance = income_total - expense_total

    # Budgets for month
    budgets = user.budgets.filter(month=month_filter).select_related('category')
    budget_items = []
    category_chart_labels = []
    category_chart_spent = []
    category_chart_budget = []

    for b in budgets:
        spent = b.spent()
        budget_items.append({
            'budget': b,
            'category': b.category,
            'limit': b.monthly_limit,
            'spent': spent,
            'pct': b.percentage_spent(),
            'is_exceeded': b.is_exceeded(),
        })
        category_chart_labels.append(b.category.name)
        category_chart_spent.append(float(spent))
        category_chart_budget.append(float(b.monthly_limit))

    recent_transactions = month_txns[:15]

    return render(request, 'finance/index.html', {
        'month_filter': month_filter,
        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'budget_items': budget_items,
        'recent_transactions': recent_transactions,
        'chart_labels': category_chart_labels,
        'chart_spent': category_chart_spent,
        'chart_budget': category_chart_budget,
    })

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            tx.save()
            messages.success(request, f"Transaction '{tx.note or tx.category}' saved.")
            return redirect('finance:index')
    else:
        form = TransactionForm(request.user)
    return render(request, 'finance/transaction_form.html', {'form': form})

@login_required
def transaction_delete(request, pk):
    tx = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        tx.delete()
        messages.success(request, "Transaction deleted.")
    return redirect('finance:index')

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, f"Budget for {budget.category.name} set.")
            return redirect('finance:index')
    else:
        form = BudgetForm(request.user)
    return render(request, 'finance/budget_form.html', {'form': form})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            messages.success(request, f"Category '{cat.name}' created.")
            return redirect('finance:index')
    else:
        form = CategoryForm()
    return render(request, 'finance/category_form.html', {'form': form})
