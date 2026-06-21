from pathlib import Path
import pandas as pd


PROCESSED_DIR = Path("data/processed")
QUALITY_DIR = Path("outputs/tables")
POWERBI_DIR = Path("outputs/tables/powerbi")

POWERBI_DIR.mkdir(parents=True, exist_ok=True)


def clean_for_powerbi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare a curated dataset for Power BI dashboarding.
    This keeps only dashboard-relevant columns and adds readable categories.
    """

    selected_columns = [
        "listing_id",
        "name",
        "host_id",
        "host_name",
        "host_is_superhost",
        "host_listings_count",
        "host_tenure_years",
        "neighbourhood",
        "latitude",
        "longitude",
        "property_type",
        "room_type",
        "accommodates",
        "bedrooms",
        "beds",
        "price_clean",
        "availability_365",
        "calendar_days",
        "available_days",
        "unavailable_days",
        "availability_rate",
        "occupancy_proxy",
        "number_of_reviews",
        "total_reviews",
        "review_scores_rating",
        "review_scores_cleanliness",
        "review_scores_location",
        "review_scores_communication",
        "estimated_revenue_proxy",
    ]

    existing_columns = [col for col in selected_columns if col in df.columns]
    powerbi_df = df[existing_columns].copy()

    # User-friendly categorical fields for dashboard filters and visuals
    powerbi_df["superhost_status"] = powerbi_df["host_is_superhost"].map({
        True: "Superhost",
        False: "Non-Superhost"
    }).fillna("Unknown")

    powerbi_df["price_status"] = powerbi_df["price_clean"].apply(
        lambda value: "Missing Price" if pd.isna(value) else "Available Price"
    )

    powerbi_df["review_status"] = powerbi_df["total_reviews"].fillna(0).apply(
        lambda value: "No Reviews" if value == 0 else "Has Reviews"
    )

    powerbi_df["availability_rate_pct"] = powerbi_df["availability_rate"] * 100
    powerbi_df["occupancy_proxy_pct"] = powerbi_df["occupancy_proxy"] * 100

    # Group hosts by listing count for portfolio analysis
    def host_segment(count):
        if pd.isna(count):
            return "Unknown"
        if count == 1:
            return "Single-listing host"
        if count <= 5:
            return "Small portfolio host"
        if count <= 20:
            return "Medium portfolio host"
        return "Large portfolio host"

    powerbi_df["host_portfolio_segment"] = powerbi_df["host_listings_count"].apply(host_segment)

    return powerbi_df


def main():
    listing_master_path = PROCESSED_DIR / "listing_master.csv"
    quality_checks_path = QUALITY_DIR / "data_quality_checks.csv"

    if not listing_master_path.exists():
        raise FileNotFoundError(
            f"Missing {listing_master_path}. Run python src/transform.py first."
        )

    listing_master = pd.read_csv(listing_master_path)
    powerbi_listing = clean_for_powerbi(listing_master)

    listing_output = POWERBI_DIR / "listing_master_powerbi.csv"
    powerbi_listing.to_csv(listing_output, index=False)

    if quality_checks_path.exists():
        quality_checks = pd.read_csv(quality_checks_path)
        quality_output = POWERBI_DIR / "data_quality_checks_powerbi.csv"
        quality_checks.to_csv(quality_output, index=False)
    else:
        quality_output = None

    print("Power BI export complete.")
    print(f"Saved: {listing_output}")

    if quality_output:
        print(f"Saved: {quality_output}")

    print("\nPower BI dataset shape:")
    print(powerbi_listing.shape)
    print("\nColumns exported:")
    print(list(powerbi_listing.columns))


if __name__ == "__main__":
    main()