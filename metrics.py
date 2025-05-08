import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_CLEAN_PATH = HERE / "clean_jobs.csv"

def load_clean_data(path=DEFAULT_CLEAN_PATH):
    return pd.read_csv(path)

def top_skills(df, skill_col="skill", n=10):
    return df[skill_col].value_counts().head(n)

def experience_distribution(df, exp_col="min_experience_years"):
    series = df[exp_col].dropna().astype(int)
    return series.value_counts().sort_index()

def salary_distribution(df, salary_col="avg_salary", bins=None):
    series = df[salary_col].dropna().astype(float)
    if bins is None:
        max_salary = int(series.max())
        bins = [0, 30000, 60000, 90000, 120000, 150000, 200000, 300000, 500000, max_salary]
    unique_bins = sorted(set(int(b) for b in bins))
    return pd.cut(series, bins=unique_bins, include_lowest=True).value_counts().sort_index()
