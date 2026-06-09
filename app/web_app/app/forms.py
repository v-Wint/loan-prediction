from django import forms
from .models import Borrower, LoanApplication


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = '__all__'


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['title', 'borrower', 'sec_borrower', 'loan_amnt', 'term', 'purpose', 'int_rate', 'issue_d']
        widgets = {
            'issue_d': forms.DateInput(attrs={'type': 'date'}),
        }

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = '__all__'
        widgets = {
            'earliest_cr_line': forms.DateInput(attrs={'type': 'date'}),
        }
