-- ============================================================
-- Inside Airbnb Market Intelligence Analysis
-- SQL Analysis Queries
-- Database: DuckDB
-- ============================================================

-- 1. Market Overview
SELECT
    COUNT(*) AS total_listings,
    COUNT(DISTINCT host_id) AS total_hosts,
    COUNT(DISTINCT neighbourhood) AS total_neighbourhoods,
    ROUND(AVG(price_clean), 2) AS avg_listing_price,
    ROUND(MEDIAN(price_clean), 2) AS median_listing_price,
    ROUND(AVG(availability_rate), 4) AS avg_availability_rate,
    ROUND(AVG(occupancy_proxy), 4) AS avg_occupancy_proxy
FROM listing_master;


-- 2. Price and Supply by Room Type
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


-- 3. Top Neighbourhoods by Average Price
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


-- 4. Neighbourhood Supply and Availability
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


-- 5. Superhost vs Non-Superhost Comparison
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


-- 6. Top Hosts by Number of Listings
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


-- 7. Review Activity by Neighbourhood
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


-- 8. Estimated Revenue Proxy by Neighbourhood
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


-- 9. Data Quality Summary
SELECT *
FROM quality_summary;