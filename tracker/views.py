from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum
from django.utils import timezone
def index(request):
    expenses = Expense.objects.all()
    total_amount = sum(expense.amount for expense in expenses)
    
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        expenses = expenses.filter(category=category)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    filtered_total_amount = sum(expense.amount for expense in expenses)

    return render(request, 'index.html', {'expenses': expenses, 'total_amount': total_amount, 'filtered_total_amount': filtered_total_amount})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    expense.delete()
    return redirect('index')

def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})




def expense_summary(request):
    
    category_totals = Expense.objects.values('category').annotate(total=Sum('amount'))

    
    today = timezone.now()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    weekly_expenses = Expense.objects.filter(date__gte=week_start)
    monthly_expenses = Expense.objects.filter(date__gte=month_start)
    yearly_expenses = Expense.objects.filter(date__gte=year_start)

    weekly_total = sum(expense.amount for expense in weekly_expenses)
    monthly_total = sum(expense.amount for expense in monthly_expenses)
    yearly_total = sum(expense.amount for expense in yearly_expenses)

    return render(request, 'expense_summary.html', {'category_totals': category_totals, 'weekly_total': weekly_total, 'monthly_total': monthly_total, 'yearly_total': yearly_total})


