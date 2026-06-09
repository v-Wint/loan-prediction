from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional

import pandas as pd
import re
import math

from src.constants import HOME_OWNERSHIP_TYPES, STATES, PURPOSE_CHOICES, TOP_50_EMP_TITLES
from src.columns import FEATURE_COLS_CLEAN


class LoanInput(BaseModel):
    loan_amnt: float
    term: int
    emp_title: Optional[str] = None
    emp_length: Optional[int] = None
    home_ownership: str = "NONE"
    annual_inc: Optional[float] = None
    verification_status: int = 0
    issue_d: date
    purpose: str
    zip_code: Optional[str] = None
    addr_state: Optional[str] = None
    dti: float
    delinq_2yrs: Optional[float] = None
    earliest_cr_line: Optional[date] = None
    fico_range_low: Optional[float] = None
    fico_range_high: Optional[float] = None
    inq_last_6mths: Optional[float] = None
    mths_since_last_delinq: Optional[float] = None
    mths_since_last_record: Optional[float] = None
    open_acc: Optional[float] = None
    pub_rec: Optional[float] = None
    revol_bal: Optional[float] = None
    revol_util: Optional[float] = None
    total_acc: Optional[float] = None
    collections_12_mths_ex_med: Optional[float] = None
    mths_since_last_major_derog: Optional[float] = None
    application_type: int = 1
    annual_inc_joint: Optional[float] = None
    dti_joint: Optional[float] = None
    verification_status_joint: Optional[int] = 0
    acc_now_delinq: Optional[float] = None
    tot_coll_amt: Optional[float] = None
    tot_cur_bal: Optional[float] = None
    open_acc_6m: Optional[float] = None
    open_act_il: Optional[float] = None
    open_il_12m: Optional[float] = None
    open_il_24m: Optional[float] = None
    mths_since_rcnt_il: Optional[float] = None
    total_bal_il: Optional[float] = None
    il_util: Optional[float] = None
    open_rv_12m: Optional[float] = None
    open_rv_24m: Optional[float] = None
    max_bal_bc: Optional[float] = None
    all_util: Optional[float] = None
    total_rev_hi_lim: Optional[float] = None
    inq_fi: Optional[float] = None
    total_cu_tl: Optional[float] = None
    inq_last_12m: Optional[float] = None
    acc_open_past_24mths: Optional[float] = None
    avg_cur_bal: Optional[float] = None
    bc_open_to_buy: Optional[float] = None
    bc_util: Optional[float] = None
    chargeoff_within_12_mths: Optional[float] = None
    delinq_amnt: Optional[float] = None
    mo_sin_old_il_acct: Optional[float] = None
    mo_sin_old_rev_tl_op: Optional[float] = None
    mo_sin_rcnt_rev_tl_op: Optional[float] = None
    mo_sin_rcnt_tl: Optional[float] = None
    mort_acc: Optional[float] = None
    mths_since_recent_bc: Optional[float] = None
    mths_since_recent_bc_dlq: Optional[float] = None
    mths_since_recent_inq: Optional[float] = None
    mths_since_recent_revol_delinq: Optional[float] = None
    num_accts_ever_120_pd: Optional[float] = None
    num_actv_bc_tl: Optional[float] = None
    num_actv_rev_tl: Optional[float] = None
    num_bc_sats: Optional[float] = None
    num_bc_tl: Optional[float] = None
    num_il_tl: Optional[float] = None
    num_op_rev_tl: Optional[float] = None
    num_rev_accts: Optional[float] = None
    num_rev_tl_bal_gt_0: Optional[float] = None
    num_sats: Optional[float] = None
    num_tl_120dpd_2m: Optional[float] = None
    num_tl_30dpd: Optional[float] = None
    num_tl_90g_dpd_24m: Optional[float] = None
    num_tl_op_past_12m: Optional[float] = None
    pct_tl_nvr_dlq: Optional[float] = None
    percent_bc_gt_75: Optional[float] = None
    pub_rec_bankruptcies: Optional[float] = None
    tax_liens: Optional[float] = None
    tot_hi_cred_lim: Optional[float] = None
    total_bal_ex_mort: Optional[float] = None
    total_bc_limit: Optional[float] = None
    total_il_high_credit_limit: Optional[float] = None
    revol_bal_joint: Optional[float] = None
    sec_app_fico_range_low: Optional[float] = None
    sec_app_fico_range_high: Optional[float] = None
    sec_app_earliest_cr_line: Optional[date] = None
    sec_app_inq_last_6mths: Optional[float] = None
    sec_app_mort_acc: Optional[float] = None
    sec_app_open_acc: Optional[float] = None
    sec_app_revol_util: Optional[float] = None
    sec_app_open_act_il: Optional[float] = None
    sec_app_num_rev_accts: Optional[float] = None
    sec_app_chargeoff_within_12_mths: Optional[float] = None
    sec_app_collections_12_mths_ex_med: Optional[float] = None
    sec_app_mths_since_last_major_derog: Optional[float] = None

    @field_validator("term", mode="before")
    @classmethod
    def parse_term(cls, v):
        if isinstance(v, str):
            return int(v.strip().split()[0])
        return v

    @field_validator("home_ownership", mode="before")
    @classmethod
    def parse_home_ownership(cls, v):
        v = str(v).upper().strip()
        if v not in HOME_OWNERSHIP_TYPES:
            raise ValueError(f"home_ownership must be one of {allowed}, got '{v}'")
        return v

    @field_validator("emp_length", mode="before")
    @classmethod
    def parse_emp_length(cls, v):
        if v is None:
            return None
        v = str(v).strip()
        if v == "< 1 year":
            return 0
        match = re.search(r"(\d+)", v)
        if not match:
            raise ValueError(f"Cannot parse emp_length from '{v}'")
        return int(match.group(1))

    @field_validator("verification_status", "verification_status_joint", mode="before")
    @classmethod
    def parse_verification_status(cls, v):
        if v is None:
            return 0
        v = str(v).strip().lower()
        if v in {"verified", "source verified"}:
            return 1
        return 0

    @field_validator("purpose", mode="before")
    @classmethod
    def parse_purpose(cls, v):
        v = str(v).strip().lower().replace(" ", "_")
        if v not in PURPOSE_CHOICES:
            raise ValueError(f"purpose must be one of {PURPOSE_CHOICES}, got '{v}'")
        return v

    @field_validator("zip_code", mode="before")
    @classmethod
    def parse_zip_code(cls, v):
        if v is None:
            return None
        v = str(v).strip()
        if len(v) < 3 or not v[:3].isdigit():
            raise ValueError(f"zip_code must start with at least 3 numeric characters, got '{v}'")
        return v[:3] + "xx"

    @field_validator("addr_state", mode="before")
    @classmethod
    def parse_addr_state(cls, v):
        if v is None:
            return None
        v = str(v).strip().upper()
        if v not in STATES:
            raise ValueError(f"addr_state must be a valid US state abbreviation, got '{v}'")
        return v

    @field_validator("application_type", mode="before")
    @classmethod
    def parse_application_type(cls, v):
        if v is None:
            return 1
        if isinstance(v, int):
            return v
        v = str(v).strip().lower()
        if v == "individual":
            return 1
        if v == "joint":
            return 0
        raise ValueError(f"application_type must be 'individual' or 'joint', got '{v}'")

    @field_validator("issue_d", "earliest_cr_line", "sec_app_earliest_cr_line", mode="before")
    @classmethod
    def parse_dates(cls, v):
        if v is None:
            return None
        if isinstance(v, float) and math.isnan(v):
            return None
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(str(v).strip(), "%b-%Y").date()
        except ValueError:
            pass
        try:
            return datetime.strptime(str(v).strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Cannot parse date from '{v}', expected formats: Jan-2024 or 2024-01-15")


    def to_df(self):
        df = pd.DataFrame([self.model_dump()])

        df['emp_title'] = df.emp_title.str.lower().str.strip()

        df.loc[~df.emp_title.isin(TOP_50_EMP_TITLES), 'emp_title'] = 'other'

        df['zip_region'] = df['zip_code'].str[0].astype('category')

        df['issue_d'] = pd.to_datetime(df['issue_d'], format="%b-%Y")
        df['earliest_cr_line'] = pd.to_datetime(df['earliest_cr_line'], format="%b-%Y")
        df['sec_app_earliest_cr_line'] = pd.to_datetime(df['sec_app_earliest_cr_line'], format="%b-%Y")

        df['issue_y'] = df['issue_d'].dt.year.astype(int)
        df['issue_m'] = df['issue_d'].dt.month.astype(int)

        df = df.rename(columns={'verification_status': 'is_verified', 'application_type': 'is_individual', 'verification_status_joint': 'is_verified_joint'})

        # with one row pandas sometimes identifies numeric columns as object
        for col in df.select_dtypes('object').columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass

        joint_cols = df.columns[df.columns.str.endswith('_joint')]
        for col in joint_cols:
            df[col[:-6]] = df[col].combine_first(df[col[:-6]])

        sec_cols = df.columns[df.columns.str.startswith('sec_app')]
        for col in sec_cols:
            df[col[8:]] = df[[col, col[8:]]].mean(axis=1, skipna=True)

        df['cr_line_y'] = df['earliest_cr_line'].dt.year.astype('Int64')
        df['cr_line_m'] = df['earliest_cr_line'].dt.month.astype('Int64')
        df['months_after_cr_line'] = (df.issue_d.dt.year - df.earliest_cr_line.dt.year) * 12 + (df.issue_d.dt.month - df.earliest_cr_line.dt.month)

        df = df.drop(columns=list(sec_cols) + list(joint_cols) + ['issue_d', 'earliest_cr_line'])

        df[df.select_dtypes('object').columns] = df.select_dtypes('object').astype('category')

        return df[FEATURE_COLS_CLEAN]
