# Inside Airbnb Market Intelligence Data Engineering Pipeline

## Project Overview

This project was completed as part of the Expernetic Data Engineer Intern technical assessment. The objective was to build a reproducible data engineering and analytics workflow using the public Inside Airbnb dataset.

The project transforms raw Airbnb market data into cleaned, validated, analytics-ready datasets and generates business insights related to listing supply, pricing, availability, host behavior, review activity, and neighbourhood-level market patterns.

## Objectives

* Understand and profile the raw Inside Airbnb dataset.
* Build a repeatable data validation, cleaning, and transformation workflow.
* Create listing-level analytical datasets from raw listings, calendar, and review files.
* Load cleaned datasets into DuckDB for SQL-based analysis.
* Design a simple dimensional model with dimension and fact tables.
* Run data quality checks and document known limitations.
* Generate SQL analysis outputs, visualizations, and statistical test results.
* Provide a reproducible project structure with clear execution steps.

## Dataset

Source: Inside Airbnb public dataset.

Selected files:

* `listings.csv.gz`
* `calendar.csv.gz`
* `reviews.csv.gz`
* `neighbourhoods.csv`
* `neighbourhoods.geojson`

The selected city dataset contains:

* 10,480 listings
* 3,825,200 calendar records
* 501,084 review records
* 22 neighbourhood records

## Key Data Limitation

During profiling, the calendar-level price column was found to be unavailable for all calendar records. Therefore, daily pricing analysis and weekend-versus-weekday price analysis were not performed.

Listing-level price from the listings file was used for price analysis, while calendar data was used only for availability and occupancy proxy calculations.

The occupancy proxy is calculated using unavailable days divided by total calendar days. This should not be interpreted as confirmed occupancy because unavailable dates may include booked dates, blocked dates, or host restrictions.

## Tools and Technologies

* Python
* Pandas
* NumPy
* DuckDB
* SQL
* Matplotlib
* SciPy
* Statsmodels
* GitHub

## Repository Structure

```text
.
├── data/
│   ├── raw/                 # Raw dataset files, not committed
│   └── processed/           # Processed outputs, not committed
├── outputs/
│   ├── figures/             # Generated charts
│   └── tables/              # Profiling, quality, SQL, and statistics outputs
├── reports/
│   ├── final_report.md
│   ├── ai_usage_disclosure.md
│   └── decision_log.md
├── sql/
│   ├── analysis_queries.sql
│   ├── create_tables.sql
│   └── quality_checks.sql
├── src/
│   ├── extract.py
│   ├── profile_data.py
│   ├── transform.py
│   ├── load.py
│   ├── quality_checks.py
│   ├── run_analysis.py
│   ├── generate_visuals.py
│   └── statistical_analysis.py
├── main.py
├── requirements.txt
└── README.md
```

## How to Run

### 1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add raw data files

Download the required city files from Inside Airbnb and place them in:

```text
data/raw/
```

Required files:

```text
listings.csv.gz
calendar.csv.gz
reviews.csv.gz
neighbourhoods.csv
neighbourhoods.geojson
```

### 4. Run the full pipeline

```bash
python main.py
```

This runs the full workflow:

1. Raw file validation
2. Data profiling
3. Data transformation
4. DuckDB loading and dimensional model creation
5. Data quality checks
6. SQL market analysis
7. Visualization generation
8. Statistical analysis

## Main Outputs

### Data Profiling

* `outputs/tables/raw_file_manifest.csv`
* `outputs/tables/dataset_summary.csv`
* `outputs/tables/data_profile.csv`

### Data Quality

* `outputs/tables/quality_summary.csv`
* `outputs/tables/data_quality_checks.csv`

### SQL Analysis

* `outputs/tables/analysis/01_market_overview.csv`
* `outputs/tables/analysis/02_room_type_summary.csv`
* `outputs/tables/analysis/03_top_neighbourhoods_by_price.csv`
* `outputs/tables/analysis/04_neighbourhood_supply_availability.csv`
* `outputs/tables/analysis/05_superhost_comparison.csv`
* `outputs/tables/analysis/06_top_hosts_by_listings.csv`
* `outputs/tables/analysis/07_review_activity_by_neighbourhood.csv`
* `outputs/tables/analysis/08_revenue_proxy_by_neighbourhood.csv`
* `outputs/tables/analysis/09_data_quality_summary.csv`

### Visualizations

* `outputs/figures/01_listing_count_by_room_type.png`
* `outputs/figures/02_average_price_by_room_type.png`
* `outputs/figures/03_top_neighbourhoods_by_average_price.png`
* `outputs/figures/04_top_neighbourhoods_by_listing_supply.png`
* `outputs/figures/05_review_activity_by_neighbourhood.png`
* `outputs/figures/06_revenue_proxy_by_neighbourhood.png`

### Statistical Analysis

* `outputs/tables/statistics/statistical_tests.csv`
* `outputs/tables/statistics/room_type_statistical_summary.csv`
* `outputs/tables/statistics/superhost_statistical_summary.csv`

## Data Model

The project creates a DuckDB analytical model with the following tables:

* `dim_listing`
* `dim_host`
* `dim_neighbourhood`
* `fact_listing_market`
* `fact_reviews`

This structure separates descriptive entities from analytical metrics and supports SQL-based business analysis.

## Key Findings

* The selected market contains 10,480 listings and 9,201 hosts.
* Entire home/apartment listings dominate the market supply.
* Average availability rate is approximately 25.77%.
* Occupancy proxy is approximately 74.23%, but this should be interpreted carefully due to calendar data limitations.
* Calendar-level prices were unavailable, so price analysis was based on listing-level price only.
* Data quality checks found no duplicate listing IDs, no invalid coordinates, and no non-positive listing prices.

## Completed Work

* Raw file validation
* Dataset profiling
* Data cleaning and standardization
* Calendar and review aggregation
* Listing master table creation
* DuckDB loading
* Dimensional model creation
* SQL market analysis
* Data quality checks
* EDA visualizations
* Statistical hypothesis tests
* Reproducible full pipeline runner

## Incomplete or De-scoped Work

The following areas were intentionally not completed due to prioritization and dataset limitations:

* Daily calendar price analysis, because calendar price values were unavailable.
* Weekend versus weekday price analysis, because daily price data was missing.
* Multi-city comparison, because the project prioritized depth over breadth.
* Machine learning price prediction, because the submission focused on data engineering quality, SQL analysis, data quality, and statistical interpretation.
* LLM/RAG experiments, because they were optional and outside the selected scope.

## AI Usage Disclosure

AI tools were used to support planning, code structure, documentation drafting, and explanation refinement. All generated code and outputs were reviewed, executed, and validated manually.

Full AI usage details are documented in:

```text
reports/ai_usage_disclosure.md
```

## Author

Data Engineer Intern Technical Assessment Submission
