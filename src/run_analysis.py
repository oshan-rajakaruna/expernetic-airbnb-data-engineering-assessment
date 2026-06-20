from pathlib import Path
import duckdb


DB_PATH = Path("data/airbnb_market.duckdb")
OUTPUT_DIR = Path("outputs/tables/analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


QUERIES = {
    "01_market_overview": """
        SELECT
            COUNT(*) AS total_listings,
            COUNT(DISTINCT host_id) AS total_hosts,
            COUNT(DISTINCT neighbourhood) AS total_neighbourhoods,
            ROUND(AVG(price_clean), 2) AS avg_listing_price,
            ROUND(MEDIAN(price_clean), 2) AS median_listing_price,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy
        FROM listing_master;
    """,

    "02_room_type_summary": """
        SELECT
            room_type,
            COUNT(*) AS listing_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS listing_share_percentage,
            ROUND(AVG(price_clean), 2) AS avg_price,
            ROUND(MEDIAN(price_clean), 2) AS median_price,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(review_scores_rating), 2) AS avg_rating
        FROM listing_master
        WHERE room_type IS NOT NULL
        GROUP BY room_type
        ORDER BY listing_count DESC;
    """,

    "03_top_neighbourhoods_by_price": """
        SELECT
            neighbourhood,
            COUNT(*) AS listing_count,
            ROUND(AVG(price_clean), 2) AS avg_price,
            ROUND(MEDIAN(price_clean), 2) AS median_price,
            ROUND(AVG(review_scores_rating), 2) AS avg_rating,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate
        FROM listing_master
        WHERE price_clean IS NOT NULL
        GROUP BY neighbourhood
        HAVING COUNT(*) >= 20
        ORDER BY avg_price DESC
        LIMIT 10;
    """,

    "04_neighbourhood_supply_availability": """
        SELECT
            neighbourhood,
            COUNT(*) AS listing_count,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
            ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy,
            ROUND(AVG(price_clean), 2) AS avg_price
        FROM listing_master
        WHERE neighbourhood IS NOT NULL
        GROUP BY neighbourhood
        ORDER BY listing_count DESC;
    """,

    "05_superhost_comparison": """
        SELECT
            host_is_superhost,
            COUNT(*) AS listing_count,
            ROUND(AVG(price_clean), 2) AS avg_price,
            ROUND(MEDIAN(price_clean), 2) AS median_price,
            ROUND(AVG(review_scores_rating), 2) AS avg_rating,
            ROUND(AVG(total_reviews), 2) AS avg_total_reviews,
            ROUND(AVG(availability_rate), 4) AS avg_availability_rate
        FROM listing_master
        WHERE host_is_superhost IS NOT NULL
        GROUP BY host_is_superhost
        ORDER BY host_is_superhost DESC;
    """,

    "06_top_hosts_by_listings": """
        SELECT
            host_id,
            host_name,
            COUNT(*) AS listing_count,
            ROUND(AVG(price_clean), 2) AS avg_price,
            ROUND(AVG(review_scores_rating), 2) AS avg_rating,
            ROUND(SUM(COALESCE(estimated_revenue_proxy, 0)), 2) AS total_estimated_revenue_proxy
        FROM listing_master
        WHERE host_id IS NOT NULL
        GROUP BY host_id, host_name
        ORDER BY listing_count DESC
        LIMIT 10;
    """,

    "07_review_activity_by_neighbourhood": """
        SELECT
            neighbourhood,
            COUNT(*) AS listing_count,
            ROUND(SUM(COALESCE(total_reviews, 0)), 0) AS total_reviews,
            ROUND(AVG(COALESCE(total_reviews, 0)), 2) AS avg_reviews_per_listing,
            ROUND(AVG(review_scores_rating), 2) AS avg_rating
        FROM listing_master
        WHERE neighbourhood IS NOT NULL
        GROUP BY neighbourhood
        ORDER BY total_reviews DESC
        LIMIT 10;
    """,

    "08_revenue_proxy_by_neighbourhood": """
        SELECT
            neighbourhood,
            COUNT(*) AS listing_count,
            ROUND(SUM(COALESCE(estimated_revenue_proxy, 0)), 2) AS estimated_revenue_proxy,
            ROUND(AVG(COALESCE(estimated_revenue_proxy, 0)), 2) AS avg_estimated_revenue_proxy_per_listing,
            ROUND(AVG(price_clean), 2) AS avg_price,
            ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy
        FROM listing_master
        WHERE neighbourhood IS NOT NULL
        GROUP BY neighbourhood
        ORDER BY estimated_revenue_proxy DESC
        LIMIT 10;
    """,

    "09_data_quality_summary": """
        SELECT *
        FROM quality_summary;
    """,
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB database not found: {DB_PATH}. Run python src/load.py first."
        )

    print("Connecting to DuckDB...")
    conn = duckdb.connect(DB_PATH.as_posix())

    for name, query in QUERIES.items():
        print(f"Running query: {name}")
        result = conn.execute(query).df()
        output_path = OUTPUT_DIR / f"{name}.csv"
        result.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")

    conn.close()
    print("\nSQL analysis complete.")


if __name__ == "__main__":
    main()