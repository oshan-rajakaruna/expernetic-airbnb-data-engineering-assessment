-- ============================================================
-- Inside Airbnb Market Intelligence
-- SQL Data Quality Checks
-- Database: DuckDB
-- ============================================================


-- 1. Duplicate listing IDs
SELECT
    'duplicate_listing_ids' AS check_name,
    COUNT(*) AS issue_count
FROM (
    SELECT listing_id
    FROM listings_clean
    GROUP BY listing_id
    HAVING COUNT(*) > 1
);


-- 2. Missing listing prices
SELECT
    'missing_listing_prices' AS check_name,
    COUNT(*) AS issue_count
FROM listings_clean
WHERE price_clean IS NULL;


-- 3. Non-positive prices
SELECT
    'non_positive_prices' AS check_name,
    COUNT(*) AS issue_count
FROM listings_clean
WHERE price_clean <= 0;


-- 4. Missing room type
SELECT
    'missing_room_type' AS check_name,
    COUNT(*) AS issue_count
FROM listings_clean
WHERE room_type IS NULL;


-- 5. Invalid coordinates
SELECT
    'invalid_coordinates' AS check_name,
    COUNT(*) AS issue_count
FROM listings_clean
WHERE latitude NOT BETWEEN -90 AND 90
   OR longitude NOT BETWEEN -180 AND 180
   OR latitude IS NULL
   OR longitude IS NULL;


-- 6. Listings without calendar summary
SELECT
    'listings_without_calendar_summary' AS check_name,
    COUNT(*) AS issue_count
FROM listing_master
WHERE calendar_days IS NULL;


-- 7. Listings without review summary
SELECT
    'listings_without_review_summary' AS check_name,
    COUNT(*) AS issue_count
FROM listing_master
WHERE total_reviews IS NULL;


-- 8. Calendar rows with missing price
-- Note: This is expected in the selected dataset.
SELECT
    'calendar_records_missing_price' AS check_name,
    COUNT(*) AS issue_count
FROM calendar_summary
WHERE calendar_price_non_null = 0;


-- 9. Availability rate outside valid range
SELECT
    'invalid_availability_rate' AS check_name,
    COUNT(*) AS issue_count
FROM calendar_summary
WHERE availability_rate < 0
   OR availability_rate > 1
   OR availability_rate IS NULL;


-- 10. Reviews without listing reference
SELECT
    'reviews_missing_listing_id' AS check_name,
    COUNT(*) AS issue_count
FROM reviews_clean
WHERE listing_id IS NULL;