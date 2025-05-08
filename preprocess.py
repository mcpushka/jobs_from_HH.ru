import re
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_DATA_PATH = HERE / "jobs.csv"
DEFAULT_CLEAN_PATH = HERE / "clean_jobs.csv"

def load_data(path=DEFAULT_DATA_PATH, encoding="utf-8", sep=","):
    return pd.read_csv(path, encoding=encoding, sep=sep)

def clean_column_names(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
    return df

def clean_skills(df, skills_col="keys"):
    df = df.copy()
    df[skills_col] = df[skills_col].fillna("").astype(str)
    def _cleanup_list(skill_list):
        cleaned = []
        for s in skill_list:
            s2 = s.strip().strip("[]'\"").lower()
            if s2:
                cleaned.append(s2)
        return cleaned
    df["skill"] = df[skills_col].str.split(r"[;,|]").apply(_cleanup_list)
    df = df.explode("skill").reset_index(drop=True)
    df = df[df["skill"].astype(bool)]
    return df

def _extract_min_years(text):
    match = re.search(r"(\d+)", str(text))
    return int(match.group(1)) if match else 0

def parse_experience(df, exp_col="experience"):
    df = df.copy()
    df[exp_col] = df[exp_col].fillna("").astype(str).str.lower()
    df["min_experience_years"] = df[exp_col].apply(_extract_min_years)
    return df

def compute_average_salary(df, min_col="from", max_col="to"):
    df = df.copy()
    df[min_col] = pd.to_numeric(df[min_col], errors="coerce")
    df[max_col] = pd.to_numeric(df[max_col], errors="coerce")
    df["avg_salary"] = df[[min_col, max_col]].mean(axis=1)
    return df

def save_csv(df, path=DEFAULT_CLEAN_PATH):
    df.to_csv(path, index=False)

if __name__ == "__main__":
    df = load_data()
    df = clean_column_names(df)
    df = clean_skills(df)
    df = parse_experience(df)
    df = compute_average_salary(df)
    keep_cols = ["employer", "name", "area", "published_at", "skill", "min_experience_years", "avg_salary"]
    df = df[keep_cols]
    save_csv(df)
    print(f"Preprocessing complete. Clean data saved to {DEFAULT_CLEAN_PATH}")
