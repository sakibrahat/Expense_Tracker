from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expense-summary/', views.expense_summary, name='expense_summary'),

    
]
