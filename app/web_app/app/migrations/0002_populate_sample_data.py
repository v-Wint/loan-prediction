from django.db import migrations
import pandas as pd
from pathlib import Path

def populate_data(apps, schema_editor):
    Borrower = apps.get_model('app', 'Borrower')
    LoanApplication = apps.get_model('app', 'LoanApplication')
    
    fixtures_path = Path(__file__).parents[1] / 'fixtures' / 'example.csv'
    df = pd.read_csv(fixtures_path)

    borrower_fields = {f.name for f in Borrower._meta.get_fields() 
                    if hasattr(f, 'column') and f.name != 'id'}
    loan_fields = {f.name for f in LoanApplication._meta.get_fields() 
                if hasattr(f, 'column') and f.name not in ('id', 'borrower', 'sec_borrower', 'created_at')}
    
    for i, row in df.iterrows():
        borrower_data = {k: v for k, v in row.items() if k in borrower_fields}
        borrower = Borrower.objects.create(**borrower_data)
        
        loan_data = {k: v for k, v in row.items() if k in loan_fields}
        title = row.get('title')
        loan_data['title'] = title if pd.notna(title) else f"Loan {i}"
        loan = LoanApplication.objects.create(borrower=borrower, **loan_data)

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(populate_data),
    ]