from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("outputs/tables")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


FILES = {
    "listings": RAW_DIR / "listings.csv.gz",
    "calendar": RAW_DIR / "calendar.csv.gz",
    "reviews": RAW_DIR / "reviews.csv.gz",
    "neighbourhoods": RAW_DIR / "neighbourhoods.csv",
}


def load_csv(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")
    return pd.read_csv(file_path, low_memory=False)


def profile_dataframe(name: str, df: pd.DataFrame) -> pd.DataFrame:
    profile = pd.DataFrame({
        "dataset": name,
        "column_name": df.columns,
        "data_type": [str(dtype) for dtype in df.dtypes],
        "non_null_count": df.notna().sum().values,
        "null_count": df.isna().sum().values,
        "null_percentage": (df.isna().mean().values * 100).round(2),
        "unique_count": df.nunique(dropna=True).values,
        "sample_value": [
            df[col].dropna().iloc[0] if df[col].dropna().shape[0] > 0 else None
            for col in df.columns
        ],
    })
    return profile


def main():
    all_profiles = []
    summary_rows = []

    for name, file_path in FILES.items():
        print(f"Reading {name}: {file_path}")
        df = load_csv(file_path)

        summary_rows.append({
            "dataset": name,
            "rows": len(df),
            "columns": len(df.columns),
            "duplicate_rows": int(df.duplicated().sum()),
            "missing_cells": int(df.isna().sum().sum()),
            "total_cells": int(df.shape[0] * df.shape[1]),
            "missing_percentage": round((df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2),
        })

        profile = profile_dataframe(name, df)
        all_profiles.append(profile)

        print(f"{name}: {len(df):,} rows, {len(df.columns)} columns")

    full_profile = pd.concat(all_profiles, ignore_index=True)
    summary = pd.DataFrame(summary_rows)

    full_profile.to_csv(OUTPUT_DIR / "data_profile.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "dataset_summary.csv", index=False)

    print("\nProfiling complete.")
    print(f"Saved: {OUTPUT_DIR / 'data_profile.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'dataset_summary.csv'}")


if __name__ == "__main__":
    main()