from django import forms
from finance.models import Transaction, Budget, Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('type', 'category', 'amount', 'date', 'note')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('category', 'monthly_limit', 'month')
        widgets = {
            'month': forms.TextInput(attrs={'placeholder': 'YYYY-MM (e.g. 2026-11)'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user, type='expense')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'type', 'color')
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
