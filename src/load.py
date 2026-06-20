from pathlib import Path
import duckdb


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/tables")
DB_PATH = Path("data/airbnb_market.duckdb")


def csv_path(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def create_table_from_csv(conn: duckdb.DuckDBPyConnection, table_name: str, file_path: Path) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing required file: {file_path}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{csv_path(file_path)}', header=True);
    """)


def main():
    print("Connecting to DuckDB...")
    conn = duckdb.connect(DB_PATH.as_posix())

    print("Loading processed CSV files into DuckDB...")

    create_table_from_csv(conn, "listings_clean", PROCESSED_DIR / "listings_clean.csv")
    create_table_from_csv(conn, "calendar_summary", PROCESSED_DIR / "calendar_summary.csv")
    create_table_from_csv(conn, "reviews_clean", PROCESSED_DIR / "reviews_clean.csv")
    create_table_from_csv(conn, "review_summary", PROCESSED_DIR / "review_summary.csv")
    create_table_from_csv(conn, "listing_master", PROCESSED_DIR / "listing_master.csv")
    create_table_from_csv(conn, "quality_summary", OUTPUT_DIR / "quality_summary.csv")

    print("Creating dimensional model tables...")

    conn.execute("""
        CREATE OR REPLACE TABLE dim_listing AS
        SELECT
            listing_id,
            name,
            property_type,
            room_type,
            accommodates,
            bedrooms,
            beds,
            minimum_nights,
            maximum_nights
        FROM listings_clean;
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE dim_host AS
        SELECT DISTINCT
            host_id,
            host_name,
            host_since,
            host_tenure_years,
            host_is_superhost,
            host_listings_count
        FROM listings_clean
        WHERE host_id IS NOT NULL;
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE dim_neighbourhood AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY neighbourhood) AS neighbourhood_key,
            neighbourhood
        FROM (
            SELECT DISTINCT neighbourhood
            FROM listings_clean
            WHERE neighbourhood IS NOT NULL
        );
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE fact_listing_market AS
        SELECT
            listing_id,
            host_id,
            neighbourhood,
            price_clean,
            availability_365,
            calendar_days,
            available_days,
            unavailable_days,
            availability_rate,
            occupancy_proxy,
            number_of_reviews,
            total_reviews,
            review_scores_rating,
            review_scores_cleanliness,
            review_scores_location,
            review_scores_communication,
            estimated_revenue_proxy
        FROM listing_master;
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE fact_reviews AS
        SELECT
            review_id,
            listing_id,
            reviewer_id,
            review_date
        FROM reviews_clean;
    """)

    print("Saving table row counts...")

    row_counts = conn.execute("""
        SELECT 'listings_clean' AS table_name, COUNT(*) AS row_count FROM listings_clean
        UNION ALL
        SELECT 'calendar_summary', COUNT(*) FROM calendar_summary
        UNION ALL
        SELECT 'reviews_clean', COUNT(*) FROM reviews_clean
        UNION ALL
        SELECT 'review_summary', COUNT(*) FROM review_summary
        UNION ALL
        SELECT 'listing_master', COUNT(*) FROM listing_master
        UNION ALL
        SELECT 'dim_listing', COUNT(*) FROM dim_listing
        UNION ALL
        SELECT 'dim_host', COUNT(*) FROM dim_host
        UNION ALL
        SELECT 'dim_neighbourhood', COUNT(*) FROM dim_neighbourhood
        UNION ALL
        SELECT 'fact_listing_market', COUNT(*) FROM fact_listing_market
        UNION ALL
        SELECT 'fact_reviews', COUNT(*) FROM fact_reviews;
    """).df()

    row_counts.to_csv(OUTPUT_DIR / "duckdb_table_row_counts.csv", index=False)

    print("\nDuckDB load complete.")
    print(f"Database created: {DB_PATH}")
    print(f"Saved: {OUTPUT_DIR / 'duckdb_table_row_counts.csv'}")
    print(row_counts)

    conn.close()


if __name__ == "__main__":
    main()