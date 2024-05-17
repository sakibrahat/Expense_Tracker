from django import forms
from .models import Expense
from django.utils import timezone

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.now().date(), label="Date")

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise forms.ValidationError("Sorry! you cannot enter future date expenses")
        return date
