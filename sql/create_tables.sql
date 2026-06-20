-- ============================================================
-- Inside Airbnb Market Intelligence
-- Analytical Table Design - DuckDB SQL
-- ============================================================
-- Purpose:
-- This script documents the analytical dimensional model used
-- for the Inside Airbnb assessment.
--
-- Tables:
-- 1. dim_listing
-- 2. dim_host
-- 3. dim_neighbourhood
-- 4. fact_listing_market
-- 5. fact_reviews
-- ============================================================


-- Dimension: Listing
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


-- Dimension: Host
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


-- Dimension: Neighbourhood
CREATE OR REPLACE TABLE dim_neighbourhood AS
SELECT
    ROW_NUMBER() OVER (ORDER BY neighbourhood) AS neighbourhood_key,
    neighbourhood
FROM (
    SELECT DISTINCT neighbourhood
    FROM listings_clean
    WHERE neighbourhood IS NOT NULL
);


-- Fact: Listing-level market metrics
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


-- Fact: Review activity
CREATE OR REPLACE TABLE fact_reviews AS
SELECT
    review_id,
    listing_id,
    reviewer_id,
    review_date
FROM reviews_clean;