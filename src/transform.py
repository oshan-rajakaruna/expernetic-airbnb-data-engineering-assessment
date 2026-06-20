from pathlib import Path
import pandas as pd
import numpy as np


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/tables")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_price(series: pd.Series) -> pd.Series:
    """
    Convert price values such as '$1,200.00' into numeric values.
    Missing or invalid values become NaN.
    """
    return (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"nan": np.nan, "None": np.nan, "": np.nan})
        .astype(float)
    )


def clean_boolean_tf(series: pd.Series) -> pd.Series:
    """
    Convert Inside Airbnb t/f values into boolean values.
    """
    return series.map({"t": True, "f": False, True: True, False: False})


def load_data():
    listings = pd.read_csv(RAW_DIR / "listings.csv.gz", low_memory=False)
    calendar = pd.read_csv(RAW_DIR / "calendar.csv.gz", low_memory=False)
    reviews = pd.read_csv(RAW_DIR / "reviews.csv.gz", low_memory=False)
    neighbourhoods = pd.read_csv(RAW_DIR / "neighbourhoods.csv", low_memory=False)

    return listings, calendar, reviews, neighbourhoods


def clean_listings(listings: pd.DataFrame) -> pd.DataFrame:
    listings = listings.copy()

    if "price" in listings.columns:
        listings["price_clean"] = clean_price(listings["price"])
    else:
        listings["price_clean"] = np.nan

    if "host_since" in listings.columns:
        listings["host_since"] = pd.to_datetime(listings["host_since"], errors="coerce")
        latest_date = pd.Timestamp.today()
        listings["host_tenure_years"] = (
            (latest_date - listings["host_since"]).dt.days / 365.25
        ).round(2)
    else:
        listings["host_tenure_years"] = np.nan

    if "host_is_superhost" in listings.columns:
        listings["host_is_superhost_clean"] = clean_boolean_tf(listings["host_is_superhost"])
    else:
        listings["host_is_superhost_clean"] = np.nan

    numeric_columns = [
        "id",
        "host_id",
        "host_listings_count",
        "latitude",
        "longitude",
        "accommodates",
        "bedrooms",
        "beds",
        "minimum_nights",
        "maximum_nights",
        "availability_365",
        "number_of_reviews",
        "review_scores_rating",
        "review_scores_cleanliness",
        "review_scores_location",
        "review_scores_communication",
    ]

    for col in numeric_columns:
        if col in listings.columns:
            listings[col] = pd.to_numeric(listings[col], errors="coerce")

    selected_columns = [
        "id",
        "name",
        "host_id",
        "host_name",
        "host_since",
        "host_tenure_years",
        "host_is_superhost_clean",
        "host_listings_count",
        "neighbourhood_cleansed",
        "latitude",
        "longitude",
        "property_type",
        "room_type",
        "accommodates",
        "bedrooms",
        "beds",
        "price_clean",
        "minimum_nights",
        "maximum_nights",
        "availability_365",
        "number_of_reviews",
        "review_scores_rating",
        "review_scores_cleanliness",
        "review_scores_location",
        "review_scores_communication",
    ]

    existing_columns = [col for col in selected_columns if col in listings.columns]
    clean = listings[existing_columns].copy()

    clean = clean.rename(columns={
        "id": "listing_id",
        "neighbourhood_cleansed": "neighbourhood",
        "host_is_superhost_clean": "host_is_superhost",
    })

    return clean


def clean_calendar(calendar: pd.DataFrame) -> pd.DataFrame:
    calendar = calendar.copy()

    calendar["date"] = pd.to_datetime(calendar["date"], errors="coerce")

    if "available" in calendar.columns:
        calendar["available_clean"] = clean_boolean_tf(calendar["available"])
    else:
        calendar["available_clean"] = np.nan

    if "price" in calendar.columns:
        calendar["price_clean"] = clean_price(calendar["price"])
    else:
        calendar["price_clean"] = np.nan

    numeric_columns = ["listing_id", "minimum_nights", "maximum_nights"]
    for col in numeric_columns:
        if col in calendar.columns:
            calendar[col] = pd.to_numeric(calendar[col], errors="coerce")

    selected_columns = [
        "listing_id",
        "date",
        "available_clean",
        "price_clean",
        "minimum_nights",
        "maximum_nights",
    ]

    existing_columns = [col for col in selected_columns if col in calendar.columns]
    clean = calendar[existing_columns].copy()

    clean = clean.rename(columns={"available_clean": "available"})

    return clean


def clean_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    reviews = reviews.copy()

    if "date" in reviews.columns:
        reviews["date"] = pd.to_datetime(reviews["date"], errors="coerce")

    numeric_columns = ["listing_id", "id", "reviewer_id"]
    for col in numeric_columns:
        if col in reviews.columns:
            reviews[col] = pd.to_numeric(reviews[col], errors="coerce")

    selected_columns = [
        "listing_id",
        "id",
        "date",
        "reviewer_id",
        "reviewer_name",
        "comments",
    ]

    existing_columns = [col for col in selected_columns if col in reviews.columns]
    clean = reviews[existing_columns].copy()

    clean = clean.rename(columns={"id": "review_id", "date": "review_date"})

    return clean


def build_calendar_summary(calendar_clean: pd.DataFrame) -> pd.DataFrame:
    summary = (
        calendar_clean
        .groupby("listing_id")
        .agg(
            calendar_days=("date", "count"),
            available_days=("available", lambda x: int((x == True).sum())),
            unavailable_days=("available", lambda x: int((x == False).sum())),
            calendar_price_non_null=("price_clean", lambda x: int(x.notna().sum())),
        )
        .reset_index()
    )

    summary["availability_rate"] = (
        summary["available_days"] / summary["calendar_days"]
    ).round(4)

    summary["occupancy_proxy"] = (
        summary["unavailable_days"] / summary["calendar_days"]
    ).round(4)

    return summary


def build_review_summary(reviews_clean: pd.DataFrame) -> pd.DataFrame:
    summary = (
        reviews_clean
        .groupby("listing_id")
        .agg(
            total_reviews=("review_id", "count"),
            first_review_date=("review_date", "min"),
            latest_review_date=("review_date", "max"),
        )
        .reset_index()
    )

    return summary


def build_listing_master(
    listings_clean: pd.DataFrame,
    calendar_summary: pd.DataFrame,
    review_summary: pd.DataFrame,
) -> pd.DataFrame:
    master = listings_clean.merge(calendar_summary, on="listing_id", how="left")
    master = master.merge(review_summary, on="listing_id", how="left")

    master["estimated_revenue_proxy"] = (
        master["price_clean"] * master["unavailable_days"]
    ).round(2)

    return master


def create_quality_summary(
    listings_clean: pd.DataFrame,
    calendar_clean: pd.DataFrame,
    reviews_clean: pd.DataFrame,
    listing_master: pd.DataFrame,
) -> pd.DataFrame:
    checks = []

    checks.append({
        "check_name": "Listings with missing price",
        "value": int(listings_clean["price_clean"].isna().sum()),
        "notes": "These records are excluded from price-based analysis."
    })

    checks.append({
        "check_name": "Listings with non-positive price",
        "value": int((listings_clean["price_clean"] <= 0).sum()),
        "notes": "Prices should be positive for meaningful market analysis."
    })

    checks.append({
        "check_name": "Duplicate listing IDs",
        "value": int(listings_clean["listing_id"].duplicated().sum()),
        "notes": "Listing ID is expected to be unique in listings."
    })

    checks.append({
        "check_name": "Calendar records with missing price",
        "value": int(calendar_clean["price_clean"].isna().sum()),
        "notes": "Calendar price is unavailable in this dataset; calendar is used for availability analysis only."
    })

    checks.append({
        "check_name": "Calendar records with missing availability",
        "value": int(calendar_clean["available"].isna().sum()),
        "notes": "Availability is required for occupancy proxy calculations."
    })

    checks.append({
        "check_name": "Reviews with missing listing ID",
        "value": int(reviews_clean["listing_id"].isna().sum()),
        "notes": "Reviews require listing_id to link back to listings."
    })

    checks.append({
        "check_name": "Listings without calendar summary",
        "value": int(listing_master["calendar_days"].isna().sum()),
        "notes": "These listings did not match calendar records."
    })

    checks.append({
        "check_name": "Listings without review summary",
        "value": int(listing_master["total_reviews"].isna().sum()),
        "notes": "These listings have no review records in the reviews file."
    })

    return pd.DataFrame(checks)


def main():
    print("Loading raw data...")
    listings, calendar, reviews, neighbourhoods = load_data()

    print("Cleaning listings...")
    listings_clean = clean_listings(listings)

    print("Cleaning calendar...")
    calendar_clean = clean_calendar(calendar)

    print("Cleaning reviews...")
    reviews_clean = clean_reviews(reviews)

    print("Building calendar summary...")
    calendar_summary = build_calendar_summary(calendar_clean)

    print("Building review summary...")
    review_summary = build_review_summary(reviews_clean)

    print("Building listing master table...")
    listing_master = build_listing_master(
        listings_clean,
        calendar_summary,
        review_summary,
    )

    print("Creating quality summary...")
    quality_summary = create_quality_summary(
        listings_clean,
        calendar_clean,
        reviews_clean,
        listing_master,
    )

    print("Saving processed outputs...")
    listings_clean.to_csv(PROCESSED_DIR / "listings_clean.csv", index=False)
    calendar_summary.to_csv(PROCESSED_DIR / "calendar_summary.csv", index=False)
    reviews_clean.to_csv(PROCESSED_DIR / "reviews_clean.csv", index=False)
    review_summary.to_csv(PROCESSED_DIR / "review_summary.csv", index=False)
    listing_master.to_csv(PROCESSED_DIR / "listing_master.csv", index=False)
    quality_summary.to_csv(OUTPUT_DIR / "quality_summary.csv", index=False)

    print("\nTransformation complete.")
    print(f"Saved: {PROCESSED_DIR / 'listings_clean.csv'}")
    print(f"Saved: {PROCESSED_DIR / 'calendar_summary.csv'}")
    print(f"Saved: {PROCESSED_DIR / 'reviews_clean.csv'}")
    print(f"Saved: {PROCESSED_DIR / 'review_summary.csv'}")
    print(f"Saved: {PROCESSED_DIR / 'listing_master.csv'}")
    print(f"Saved: {OUTPUT_DIR / 'quality_summary.csv'}")


if __name__ == "__main__":
    main()