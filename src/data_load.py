import pandas as pd
from pathlib import Path

from src.columns import CLASS_TARGET, REG_TARGET, FEATURE_COLS_CLEAN, INFO_COLS, set_0_cols, set_100_cols
from src.constants import EMP_TITLE_MAPPING



def load_data(path=(Path(__file__).parent.parent / 'data' / 'accepted.csv.gz').resolve()):
    category_columns = ['grade', 'sub_grade', 'emp_title', 'home_ownership', 'verification_status', 'verification_status_joint', 'purpose', 'zip_code', 'addr_state', 'settlement_status', 'loan_status']

    exclude_columns = ['id', 'member_id', 'pymnt_plan', 'url', 'desc', 'title', 'initial_list_status', 'next_pymnt_d', 'initial_list_status', 'hardship_flag', 'hardship_type', 'hardship_reason', 'hardship_status', 'hardship_amount', 'hardship_start_date', 'hardship_end_date', 'hardship_length', 'hardship_dpd', 'hardship_loan_status', 'hardship_payoff_balance_amount', 'hardship_last_payment_amount', 'deferral_term', 'orig_projected_additional_accrued_interest', 'payment_plan_start_date', 'disbursement_method']

    date_columns = ["issue_d", "earliest_cr_line", "last_pymnt_d", "last_credit_pull_d", "debt_settlement_flag_date", "settlement_date", 'sec_app_earliest_cr_line']


    df = pd.read_csv(
        path,
        date_format="%b-%Y",
        parse_dates=date_columns,
        usecols=lambda x: x not in exclude_columns,
        dtype={x: 'category' for x in category_columns}
    )

    default_categories = ['Charged Off', 'Default', 'Does not meet the credit policy. Status:Charged Off']
    paid_categories = ['Fully Paid', 'Does not meet the credit policy. Status:Fully Paid']
    df = df[df['loan_status'].isin(default_categories + paid_categories)].copy()
    df['is_default'] = df.loan_status.isin(default_categories).astype(int)


    df['term'] = df.term.str.split().str.get(0).astype(int)

    df['emp_title'] = df.emp_title.str.lower().str.strip()
    top_50_empl_titles = df['emp_title'].dropna().map(EMP_TITLE_MAPPING).fillna(df.emp_title).value_counts().head(50).index.values
    df.loc[~df.emp_title.isin(top_50_empl_titles), 'emp_title'] = 'other'
    df['emp_title'] = df['emp_title'].astype('category')

    df['emp_length'] = df['emp_length'].replace('< 1 year', '0').str.extract(r"(\d+)").astype("Int64")

    df['verification_status'] = df.verification_status.isin(['Source Verified', 'Verified']).astype(int)
    df = df.rename(columns={'verification_status': 'is_verified'})

    df['zip_region'] = df['zip_code'].str[0].astype('category')


    df['issue_y'] = df['issue_d'].dt.year.astype(int)
    df['issue_m'] = df['issue_d'].dt.month.astype(int)

    df['application_type'] = (df.application_type == 'Individual').astype(int)
    df = df.rename(columns={'application_type': 'is_individual'})


    df['verification_status_joint'] = df.verification_status_joint.isin(['Source Verified', 'Verified']).astype(int)
    df = df.rename(columns={'verification_status_joint': 'is_verified_joint'})


    joint_cols = df.columns[df.columns.str.endswith('_joint')]
    for col in joint_cols:
        df[col[:-6]] = df[col].combine_first(df[col[:-6]])
    df = df.drop(columns=joint_cols)


    sec_cols = df.columns[df.columns.str.startswith('sec_app')]
    df['sec_app_earliest_cr_line'] = pd.to_datetime(df['sec_app_earliest_cr_line'], format="%b-%Y")
    for col in sec_cols:
        df[col[8:]] = df[[col, col[8:]]].mean(axis=1, skipna=True)
    df = df.drop(columns=sec_cols)



    df['cr_line_y'] = df['earliest_cr_line'].dt.year.astype('Int64')
    df['cr_line_m'] = df['earliest_cr_line'].dt.month.astype('Int64')
    df['months_after_cr_line'] = (df.issue_d.dt.year - df.earliest_cr_line.dt.year) * 12 + (df.issue_d.dt.month - df.earliest_cr_line.dt.month)


    df['debt_settlement_flag'] = (df.debt_settlement_flag == 'Y').astype(int)

    df['net_return'] = df.total_pymnt - df.loan_amnt
    df['ann_return'] = (df.total_pymnt / df.loan_amnt) ** (12 / df.term) - 1

    df = df[CLASS_TARGET + REG_TARGET + FEATURE_COLS_CLEAN + INFO_COLS]

    df = df.dropna(subset=['inq_last_6mths', 'zip_code'])


    df[set_0_cols] = df[set_0_cols].fillna(0)
    df[set_100_cols] = df[set_100_cols].fillna(100)


    df['dti'] = df['dti'].replace(-1, df['dti'].mean())

    return df
