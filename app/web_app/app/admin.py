from django.contrib import admin
from .models import Borrower, LoanApplication

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'addr_state', 'fico_range_low', 'annual_inc', 'dti']
    search_fields = ['name', 'addr_state']

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'purpose', 'loan_amnt', 'decision', 'confidence', 'created_at']
    search_fields = ['title', 'purpose']
    list_filter = ['decision', 'purpose']
