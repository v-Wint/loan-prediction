from django.db import models
from django.core.exceptions import ValidationError


import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR.parent))

from src.constants import HOME_OWNERSHIP_TYPES, STATES, PURPOSE_CHOICES
from src.loan_input import LoanInput


class Borrower(models.Model):
    name = models.CharField(max_length=100, verbose_name='Full Name')
    annual_inc = models.FloatField(verbose_name='Annual Income ($)')
    emp_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Employment Title')
    emp_length = models.IntegerField(null=True, blank=True, verbose_name='Employment Length (years)')
    home_ownership = models.CharField(max_length=10, choices=[(x, x.title()) for x in HOME_OWNERSHIP_TYPES], verbose_name='Home Ownership')
    verification_status = models.CharField(max_length=20, choices=[("Not Verified", "Not verified"), ("Verified", "Verified"), ("Source Verified", "Source verified")], verbose_name='Verification Status')
    zip_code = models.CharField(max_length=5, null=True, blank=True, verbose_name='ZIP Code')
    addr_state = models.CharField(max_length=2, null=True, blank=True, choices=[(x, x) for x in sorted(STATES)], verbose_name='State')

    dti = models.FloatField(verbose_name='Debt-to-Income Ratio (%)')
    delinq_2yrs = models.FloatField(null=True, blank=True, verbose_name='Delinquencies (last 2 years)')
    earliest_cr_line = models.DateField(null=True, blank=True, verbose_name='Earliest Credit Line')

    fico_range_low = models.FloatField(null=True, blank=True, verbose_name='FICO Score (low)')
    fico_range_high = models.FloatField(null=True, blank=True, verbose_name='FICO Score (high)')

    inq_last_6mths = models.FloatField(null=True, blank=True, verbose_name='Credit Inquiries (last 6 months)')
    mths_since_last_delinq = models.FloatField(null=True, blank=True, verbose_name='Months Since Last Delinquency')
    mths_since_last_record = models.FloatField(null=True, blank=True, verbose_name='Months Since Last Public Record')
    open_acc = models.FloatField(null=True, blank=True, verbose_name='Open Credit Accounts')
    pub_rec = models.FloatField(null=True, blank=True, verbose_name='Public Records')
    revol_bal = models.FloatField(null=True, blank=True, verbose_name='Revolving Balance ($)')
    revol_util = models.FloatField(null=True, blank=True, verbose_name='Revolving Utilization (%)')
    total_acc = models.FloatField(null=True, blank=True, verbose_name='Total Credit Accounts')
    collections_12_mths_ex_med = models.FloatField(null=True, blank=True, verbose_name='Collections ex. Medical (last 12 months)')
    mths_since_last_major_derog = models.FloatField(null=True, blank=True, verbose_name='Months Since Last Major Derogatory')
    acc_now_delinq = models.FloatField(null=True, blank=True, verbose_name='Accounts Currently Delinquent')
    tot_coll_amt = models.FloatField(null=True, blank=True, verbose_name='Total Collection Amount ($)')
    tot_cur_bal = models.FloatField(null=True, blank=True, verbose_name='Total Current Balance ($)')
    open_acc_6m = models.FloatField(null=True, blank=True, verbose_name='Open Accounts (last 6 months)')
    open_act_il = models.FloatField(null=True, blank=True, verbose_name='Open Active Installment Accounts')
    open_il_12m = models.FloatField(null=True, blank=True, verbose_name='Installment Accounts Opened (last 12 months)')
    open_il_24m = models.FloatField(null=True, blank=True, verbose_name='Installment Accounts Opened (last 24 months)')
    mths_since_rcnt_il = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Installment')
    total_bal_il = models.FloatField(null=True, blank=True, verbose_name='Total Installment Balance ($)')
    il_util = models.FloatField(null=True, blank=True, verbose_name='Installment Utilization (%)')
    open_rv_12m = models.FloatField(null=True, blank=True, verbose_name='Revolving Accounts Opened (last 12 months)')
    open_rv_24m = models.FloatField(null=True, blank=True, verbose_name='Revolving Accounts Opened (last 24 months)')
    max_bal_bc = models.FloatField(null=True, blank=True, verbose_name='Max Balance on Bankcard ($)')
    all_util = models.FloatField(null=True, blank=True, verbose_name='All Accounts Utilization (%)')
    total_rev_hi_lim = models.FloatField(null=True, blank=True, verbose_name='Total Revolving Credit Limit ($)')
    inq_fi = models.FloatField(null=True, blank=True, verbose_name='Finance Inquiries')
    total_cu_tl = models.FloatField(null=True, blank=True, verbose_name='Total Credit Union Tradelines')
    inq_last_12m = models.FloatField(null=True, blank=True, verbose_name='Credit Inquiries (last 12 months)')
    acc_open_past_24mths = models.FloatField(null=True, blank=True, verbose_name='Accounts Opened (last 24 months)')
    avg_cur_bal = models.FloatField(null=True, blank=True, verbose_name='Average Current Balance ($)')
    bc_open_to_buy = models.FloatField(null=True, blank=True, verbose_name='Bankcard Open to Buy ($)')
    bc_util = models.FloatField(null=True, blank=True, verbose_name='Bankcard Utilization (%)')
    chargeoff_within_12_mths = models.FloatField(null=True, blank=True, verbose_name='Charge-offs (last 12 months)')
    delinq_amnt = models.FloatField(null=True, blank=True, verbose_name='Delinquent Amount ($)')
    mo_sin_old_il_acct = models.FloatField(null=True, blank=True, verbose_name='Months Since Oldest Installment Account')
    mo_sin_old_rev_tl_op = models.FloatField(null=True, blank=True, verbose_name='Months Since Oldest Revolving Account')
    mo_sin_rcnt_rev_tl_op = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Revolving Account')
    mo_sin_rcnt_tl = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Account')
    mort_acc = models.FloatField(null=True, blank=True, verbose_name='Mortgage Accounts')
    mths_since_recent_bc = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Bankcard')
    mths_since_recent_bc_dlq = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Bankcard Delinquency')
    mths_since_recent_inq = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Inquiry')
    mths_since_recent_revol_delinq = models.FloatField(null=True, blank=True, verbose_name='Months Since Most Recent Revolving Delinquency')
    num_accts_ever_120_pd = models.FloatField(null=True, blank=True, verbose_name='Accounts Ever 120+ Days Past Due')
    num_actv_bc_tl = models.FloatField(null=True, blank=True, verbose_name='Active Bankcard Accounts')
    num_actv_rev_tl = models.FloatField(null=True, blank=True, verbose_name='Active Revolving Accounts')
    num_bc_sats = models.FloatField(null=True, blank=True, verbose_name='Satisfactory Bankcard Accounts')
    num_bc_tl = models.FloatField(null=True, blank=True, verbose_name='Bankcard Accounts')
    num_il_tl = models.FloatField(null=True, blank=True, verbose_name='Installment Accounts')
    num_op_rev_tl = models.FloatField(null=True, blank=True, verbose_name='Open Revolving Accounts')
    num_rev_accts = models.FloatField(null=True, blank=True, verbose_name='Revolving Accounts')
    num_rev_tl_bal_gt_0 = models.FloatField(null=True, blank=True, verbose_name='Revolving Accounts with Balance > $0')
    num_sats = models.FloatField(null=True, blank=True, verbose_name='Satisfactory Accounts')
    num_tl_120dpd_2m = models.FloatField(null=True, blank=True, verbose_name='Accounts 120+ DPD (last 2 months)')
    num_tl_30dpd = models.FloatField(null=True, blank=True, verbose_name='Accounts 30+ DPD')
    num_tl_90g_dpd_24m = models.FloatField(null=True, blank=True, verbose_name='Accounts 90+ DPD (last 24 months)')
    num_tl_op_past_12m = models.FloatField(null=True, blank=True, verbose_name='Accounts Opened (last 12 months)')
    pct_tl_nvr_dlq = models.FloatField(null=True, blank=True, verbose_name='% Accounts Never Delinquent')
    percent_bc_gt_75 = models.FloatField(null=True, blank=True, verbose_name='% Bankcards > 75% Utilization')
    pub_rec_bankruptcies = models.FloatField(null=True, blank=True, verbose_name='Public Record Bankruptcies')
    tax_liens = models.FloatField(null=True, blank=True, verbose_name='Tax Liens')
    tot_hi_cred_lim = models.FloatField(null=True, blank=True, verbose_name='Total High Credit Limit ($)')
    total_bal_ex_mort = models.FloatField(null=True, blank=True, verbose_name='Total Balance ex. Mortgage ($)')
    total_bc_limit = models.FloatField(null=True, blank=True, verbose_name='Total Bankcard Limit ($)')
    total_il_high_credit_limit = models.FloatField(null=True, blank=True, verbose_name='Total Installment High Credit Limit ($)')

    def clean(self):
        if self.home_ownership not in HOME_OWNERSHIP_TYPES:
            raise ValidationError({'home_ownership': 'Invalid home ownership value'})
        if self.addr_state and self.addr_state not in STATES:
            raise ValidationError({'addr_state': 'Invalid state abbreviation'})
        if self.zip_code and not (len(self.zip_code) >= 5 and self.zip_code[:3].isdigit()):
            raise ValidationError({'zip_code': 'Invalid zip code'})

    def __str__(self):
        return f"{self.name} from {self.addr_state} FICO {self.fico_range_low}"



class LoanApplication(models.Model):
    title = models.CharField(max_length=50, verbose_name='Loan Title')
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='loans', verbose_name='Primary Borrower')
    sec_borrower = models.ForeignKey(Borrower, null=True, blank=True, on_delete=models.CASCADE, related_name='sec_loans', verbose_name='Secondary Borrower')
    loan_amnt = models.FloatField(verbose_name='Loan Amount ($)')
    term = models.IntegerField(verbose_name='Term (months)')
    purpose = models.CharField(max_length=50, choices=[(x, x.replace("_", " ").capitalize()) for x in PURPOSE_CHOICES], verbose_name='Purpose')
    int_rate = models.FloatField(verbose_name='Interest rate (%)')
    issue_d = models.DateField(verbose_name='Issue Date')
    decision = models.CharField(max_length=10, null=True, blank=True, verbose_name='Decision')
    confidence = models.FloatField(null=True, blank=True, verbose_name='Degree of confidence in the decision (%)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def to_loan_input(self):
        b = self.borrower
        s = self.sec_borrower

        data = {k: v for k, v in b.__dict__.items()
                if k in LoanInput.model_fields and not k.startswith('_')}

        data.update({
            'loan_amnt': self.loan_amnt,
            'term': self.term,
            'purpose': self.purpose,
            'issue_d': self.issue_d,
        })

        if s:
            data.update({
                'application_type': 0,
                'annual_inc_joint': b.annual_inc + s.annual_inc,
                'dti_joint': s.dti,
                'verification_status_joint': max(b.verification_status, s.verification_status),
                'sec_app_fico_range_low': s.fico_range_low,
                'sec_app_fico_range_high': s.fico_range_high,
                'sec_app_earliest_cr_line': s.earliest_cr_line,
            })
        else:
            data['application_type'] = 1

        loan_input = LoanInput(**data)
        return loan_input

    def clean(self):
       if self.purpose not in PURPOSE_CHOICES:
            raise ValidationError({'purpose': 'Invalid purpose value'})

    def __str__(self):
        return f"Loan {self.title} ({self.id}) — {self.purpose} ${self.loan_amnt}"
