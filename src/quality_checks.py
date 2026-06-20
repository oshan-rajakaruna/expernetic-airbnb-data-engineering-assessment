from pathlib import Path
import duckdb
import pandas as pd


DB_PATH = Path("data/airbnb_market.duckdb")
OUTPUT_DIR = Path("outputs/tables")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


QUALITY_CHECKS = {
    "duplicate_listing_ids": """
        SELECT COUNT(*) AS issue_count
        FROM (
            SELECT listing_id
            FROM listings_clean
            GROUP BY listing_id
            HAVING COUNT(*) > 1
        );
    """,

    "missing_listing_prices": """
        SELECT COUNT(*) AS issue_count
        FROM listings_clean
        WHERE price_clean IS NULL;
    """,

    "non_positive_prices": """
        SELECT COUNT(*) AS issue_count
        FROM listings_clean
        WHERE price_clean <= 0;
    """,

    "missing_room_type": """
        SELECT COUNT(*) AS issue_count
        FROM listings_clean
        WHERE room_type IS NULL;
    """,

    "invalid_coordinates": """
        SELECT COUNT(*) AS issue_count
        FROM listings_clean
        WHERE latitude NOT BETWEEN -90 AND 90
           OR longitude NOT BETWEEN -180 AND 180
           OR latitude IS NULL
           OR longitude IS NULL;
    """,

    "listings_without_calendar_summary": """
        SELECT COUNT(*) AS issue_count
        FROM listing_master
        WHERE calendar_days IS NULL;
    """,

    "listings_without_review_summary": """
        SELECT COUNT(*) AS issue_count
        FROM listing_master
        WHERE total_reviews IS NULL;
    """,

    "calendar_records_missing_price": """
        SELECT COUNT(*) AS issue_count
        FROM calendar_summary
        WHERE calendar_price_non_null = 0;
    """,

    "invalid_availability_rate": """
        SELECT COUNT(*) AS issue_count
        FROM calendar_summary
        WHERE availability_rate < 0
           OR availability_rate > 1
           OR availability_rate IS NULL;
    """,

    "reviews_missing_listing_id": """
        SELECT COUNT(*) AS issue_count
        FROM reviews_clean
        WHERE listing_id IS NULL;
    """,
}


EXPECTED_ISSUES = {
    "missing_listing_prices",
    "listings_without_review_summary",
    "calendar_records_missing_price",
}


def classify_status(check_name: str, issue_count: int) -> str:
    if issue_count == 0:
        return "pass"

    if check_name in EXPECTED_ISSUES:
        return "warning_expected"

    return "fail"


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB database not found: {DB_PATH}. Run python src/load.py first."
        )

    conn = duckdb.connect(DB_PATH.as_posix())

    rows = []

    for check_name, query in QUALITY_CHECKS.items():
        issue_count = conn.execute(query).fetchone()[0]
        status = classify_status(check_name, int(issue_count))

        rows.append({
            "check_name": check_name,
            "issue_count": int(issue_count),
            "status": status,
        })

    conn.close()

    results = pd.DataFrame(rows)
    output_path = OUTPUT_DIR / "data_quality_checks.csv"
    results.to_csv(output_path, index=False)

    print("Data quality checks complete.")
    print(f"Saved: {output_path}")
    print(results)


if __name__ == "__main__":
    main()