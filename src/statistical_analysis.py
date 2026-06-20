from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/tables/statistics")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def cohen_d(group_a: pd.Series, group_b: pd.Series) -> float:
    group_a = group_a.dropna()
    group_b = group_b.dropna()

    n1 = len(group_a)
    n2 = len(group_b)

    if n1 < 2 or n2 < 2:
        return np.nan

    pooled_std = np.sqrt(
        ((n1 - 1) * group_a.var(ddof=1) + (n2 - 1) * group_b.var(ddof=1))
        / (n1 + n2 - 2)
    )

    if pooled_std == 0:
        return np.nan

    return round((group_a.mean() - group_b.mean()) / pooled_std, 4)


def mann_whitney_test(
    test_name: str,
    group_a_name: str,
    group_b_name: str,
    group_a: pd.Series,
    group_b: pd.Series,
    metric: str,
    business_question: str,
) -> dict:
    group_a = group_a.dropna()
    group_b = group_b.dropna()

    statistic, p_value = stats.mannwhitneyu(
        group_a,
        group_b,
        alternative="two-sided"
    )

    return {
        "test_name": test_name,
        "business_question": business_question,
        "metric": metric,
        "test_used": "Mann-Whitney U test",
        "null_hypothesis": f"{group_a_name} and {group_b_name} have the same distribution for {metric}.",
        "alternative_hypothesis": f"{group_a_name} and {group_b_name} have different distributions for {metric}.",
        "group_a": group_a_name,
        "group_b": group_b_name,
        "group_a_count": len(group_a),
        "group_b_count": len(group_b),
        "group_a_mean": round(group_a.mean(), 4),
        "group_b_mean": round(group_b.mean(), 4),
        "group_a_median": round(group_a.median(), 4),
        "group_b_median": round(group_b.median(), 4),
        "test_statistic": round(statistic, 4),
        "p_value": round(p_value, 6),
        "effect_size_cohens_d": cohen_d(group_a, group_b),
        "interpretation": "Significant difference" if p_value < 0.05 else "No statistically significant difference",
        "method_note": "Mann-Whitney U was used because Airbnb price and rating distributions are often skewed and may violate normality assumptions.",
    }


def kruskal_test(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    min_group_size: int = 30,
) -> dict:
    filtered = df[[group_col, value_col]].dropna()

    group_sizes = filtered.groupby(group_col).size()
    valid_groups = group_sizes[group_sizes >= min_group_size].index

    filtered = filtered[filtered[group_col].isin(valid_groups)]

    grouped_values = [
        group[value_col].dropna()
        for _, group in filtered.groupby(group_col)
    ]

    statistic, p_value = stats.kruskal(*grouped_values)

    n = len(filtered)
    k = len(grouped_values)

    epsilon_squared = (statistic - k + 1) / (n - k) if n > k else np.nan

    return {
        "test_name": "Neighbourhood price difference",
        "business_question": "Do listing prices differ significantly across neighbourhoods?",
        "metric": value_col,
        "test_used": "Kruskal-Wallis H test",
        "null_hypothesis": "Neighbourhood groups have the same price distribution.",
        "alternative_hypothesis": "At least one neighbourhood has a different price distribution.",
        "group_a": "Neighbourhood groups",
        "group_b": "Not applicable",
        "group_a_count": n,
        "group_b_count": k,
        "group_a_mean": round(filtered[value_col].mean(), 4),
        "group_b_mean": np.nan,
        "group_a_median": round(filtered[value_col].median(), 4),
        "group_b_median": np.nan,
        "test_statistic": round(statistic, 4),
        "p_value": round(p_value, 6),
        "effect_size_cohens_d": np.nan,
        "effect_size_epsilon_squared": round(epsilon_squared, 4),
        "interpretation": "Significant difference" if p_value < 0.05 else "No statistically significant difference",
        "method_note": "Kruskal-Wallis was used as a non-parametric alternative to ANOVA because prices are typically skewed and grouped by multiple neighbourhoods.",
    }


def main():
    master_path = PROCESSED_DIR / "listing_master.csv"

    if not master_path.exists():
        raise FileNotFoundError(
            f"Missing {master_path}. Run python src/transform.py first."
        )

    df = pd.read_csv(master_path)

    results = []

    # H1: Entire home/apt vs Private room prices
    entire_home_prices = df.loc[
        df["room_type"] == "Entire home/apt", "price_clean"
    ]

    private_room_prices = df.loc[
        df["room_type"] == "Private room", "price_clean"
    ]

    results.append(
        mann_whitney_test(
            test_name="Room type price difference",
            group_a_name="Entire home/apt",
            group_b_name="Private room",
            group_a=entire_home_prices,
            group_b=private_room_prices,
            metric="price_clean",
            business_question="Do entire-home listings command different prices than private rooms?",
        )
    )

    # H2: Superhost vs non-superhost ratings
    superhost_ratings = df.loc[
        df["host_is_superhost"] == True, "review_scores_rating"
    ]

    non_superhost_ratings = df.loc[
        df["host_is_superhost"] == False, "review_scores_rating"
    ]

    results.append(
        mann_whitney_test(
            test_name="Superhost rating difference",
            group_a_name="Superhost listings",
            group_b_name="Non-superhost listings",
            group_a=superhost_ratings,
            group_b=non_superhost_ratings,
            metric="review_scores_rating",
            business_question="Do superhost listings achieve different review ratings than non-superhost listings?",
        )
    )

    # H3: High-review vs low-review listing prices
    high_review_prices = df.loc[
        df["total_reviews"].fillna(0) > 10, "price_clean"
    ]

    low_review_prices = df.loc[
        df["total_reviews"].fillna(0) <= 10, "price_clean"
    ]

    results.append(
        mann_whitney_test(
            test_name="Review count price difference",
            group_a_name="Listings with more than 10 reviews",
            group_b_name="Listings with 10 or fewer reviews",
            group_a=high_review_prices,
            group_b=low_review_prices,
            metric="price_clean",
            business_question="Do listings with higher review activity have different prices?",
        )
    )

    # H4: Neighbourhood price differences
    neighbourhood_result = kruskal_test(
        df=df,
        group_col="neighbourhood",
        value_col="price_clean",
        min_group_size=30,
    )

    if "effect_size_epsilon_squared" not in results[0]:
        for item in results:
            item["effect_size_epsilon_squared"] = np.nan

    results.append(neighbourhood_result)

    results_df = pd.DataFrame(results)

    output_path = OUTPUT_DIR / "statistical_tests.csv"
    results_df.to_csv(output_path, index=False)

    # Additional group summaries for report writing
    room_type_summary = (
        df.groupby("room_type")
        .agg(
            listing_count=("listing_id", "count"),
            avg_price=("price_clean", "mean"),
            median_price=("price_clean", "median"),
            avg_rating=("review_scores_rating", "mean"),
            avg_total_reviews=("total_reviews", "mean"),
        )
        .round(4)
        .reset_index()
    )

    room_type_summary.to_csv(
        OUTPUT_DIR / "room_type_statistical_summary.csv",
        index=False,
    )

    superhost_summary = (
        df.groupby("host_is_superhost")
        .agg(
            listing_count=("listing_id", "count"),
            avg_price=("price_clean", "mean"),
            median_price=("price_clean", "median"),
            avg_rating=("review_scores_rating", "mean"),
            avg_total_reviews=("total_reviews", "mean"),
        )
        .round(4)
        .reset_index()
    )

    superhost_summary.to_csv(
        OUTPUT_DIR / "superhost_statistical_summary.csv",
        index=False,
    )

    print("Statistical analysis complete.")
    print(f"Saved: {output_path}")
    print(results_df[[
        "test_name",
        "test_used",
        "p_value",
        "interpretation",
        "effect_size_cohens_d",
        "effect_size_epsilon_squared",
    ]])


if __name__ == "__main__":
    main()