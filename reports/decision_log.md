# Engineering Decision Log

## Project: Inside Airbnb Market Intelligence Data Engineering Pipeline

This document records the key engineering, analytical, and prioritization decisions made during the project.

---

## Decision 1: Use One City Dataset Instead of Multiple Cities

### Decision

I selected one city dataset from Inside Airbnb and focused on depth rather than multi-city breadth.

### Options Considered

* Analyze one city deeply.
* Analyze two or more cities for comparison.
* Build a generalized multi-city pipeline.

### Reasoning

The assignment scope was intentionally broad, and the evaluation emphasized quality, reasoning, prioritization, and communication. A one-city approach allowed more time to build a clean data pipeline, perform profiling, implement data quality checks, create a dimensional model, run SQL analysis, and document limitations properly.

### Trade-off

This reduced cross-city comparison opportunities, but improved depth, reproducibility, and analytical clarity.

---

## Decision 2: Use Python and Pandas for Data Processing

### Decision

I used Python with Pandas for ingestion, profiling, cleaning, transformation, and aggregation.

### Options Considered

* Python with Pandas
* PySpark
* dbt
* SQL-only processing

### Reasoning

Pandas was appropriate for the selected dataset size and allowed rapid development of readable, testable transformation logic. It was also suitable for a local, reproducible take-home assessment.

### Trade-off

Pandas may not be the best option for very large-scale production pipelines. For a 50+ city production scenario, PySpark, cloud data processing, or distributed execution would be more suitable.

---

## Decision 3: Use DuckDB as the Analytical Database

### Decision

I loaded cleaned datasets into DuckDB and created analytical tables.

### Options Considered

* DuckDB
* SQLite
* PostgreSQL
* BigQuery or Snowflake

### Reasoning

DuckDB is lightweight, fast for analytical SQL, easy to run locally, and does not require server setup. It is a strong fit for a reproducible assessment environment.

### Trade-off

DuckDB is excellent for local analytics, but a production deployment may require a managed warehouse such as BigQuery, Snowflake, Redshift, or PostgreSQL depending on scale and access requirements.

---

## Decision 4: Build a Listing-Level Master Table

### Decision

I created `listing_master.csv` by joining cleaned listing attributes with calendar summary metrics and review summary metrics.

### Options Considered

* Analyze each raw file separately.
* Create one wide listing-level analytical table.
* Create only normalized dimension and fact tables.

### Reasoning

A listing-level master table makes analysis easier because each listing has one row with pricing, availability, review, host, and neighbourhood attributes. This simplified SQL analysis, visualization, and statistical testing.

### Trade-off

The master table is denormalized and may contain some repeated host/neighbourhood attributes. To balance this, I also created separate dimension and fact tables in DuckDB.

---

## Decision 5: Aggregate Calendar Data at Listing Level

### Decision

I aggregated the calendar file into `calendar_summary.csv` with metrics such as calendar days, available days, unavailable days, availability rate, and occupancy proxy.

### Options Considered

* Keep daily calendar rows for all analysis.
* Aggregate calendar data by listing.
* Aggregate calendar data by neighbourhood and date.

### Reasoning

The calendar file contained more than 3.8 million rows. Aggregating it to listing level made the dataset easier to analyze while preserving important availability indicators.

### Trade-off

Daily seasonality analysis became less detailed. However, the selected dataset did not contain usable daily price values, so deeper calendar price analysis was not appropriate.

---

## Decision 6: Treat Calendar Price as a Data Limitation

### Decision

I did not use calendar-level price for analysis because the calendar price field was missing for all calendar summary records.

### Options Considered

* Impute daily prices.
* Use listing-level price as a daily price substitute.
* Exclude calendar price analysis and document the limitation.

### Reasoning

Imputing daily prices would introduce unsupported assumptions. Listing-level price may not represent daily dynamic pricing accurately. Therefore, I used listing-level price only for listing price analysis and used calendar data only for availability and occupancy proxy calculations.

### Trade-off

Weekend versus weekday price analysis and seasonal daily price analysis were de-scoped. This improved honesty and reduced the risk of misleading conclusions.

---

## Decision 7: Use Occupancy Proxy Carefully

### Decision

I calculated occupancy proxy as unavailable days divided by total calendar days.

### Reasoning

Calendar availability can indicate market demand, but unavailable dates may represent bookings, host-blocked dates, maintenance, or platform restrictions. Therefore, I treated this as a proxy rather than confirmed occupancy.

### Trade-off

The metric provides useful directional insight but should not be interpreted as exact occupancy.

---

## Decision 8: Use Non-Parametric Statistical Tests

### Decision

I used Mann-Whitney U tests for two-group comparisons and Kruskal-Wallis tests for neighbourhood price differences.

### Options Considered

* Independent t-tests and ANOVA
* Mann-Whitney U and Kruskal-Wallis
* Descriptive statistics only

### Reasoning

Airbnb price distributions are typically skewed and may violate normality assumptions. Non-parametric tests are more appropriate for comparing skewed distributions.

### Trade-off

Non-parametric tests are less focused on comparing means directly, but they are more robust for skewed real-world data.

---

## Decision 9: De-scope Machine Learning and LLM/RAG Experiments

### Decision

I did not implement full machine learning price prediction, RAG, or AI agent components.

### Reasoning

The role is Data Engineer Intern, and the strongest use of time was to focus on data profiling, cleaning, quality checks, modeling, SQL analysis, reproducibility, and business interpretation.

### Trade-off

This reduced optional advanced scope, but improved the quality and completeness of the core data engineering submission.

---

## Decision 10: Commit Generated Analysis Outputs but Exclude Raw and Processed Data

### Decision

I excluded raw data, processed data, virtual environment files, and DuckDB database files from Git, while committing small analysis outputs and figures.

### Reasoning

Raw and processed datasets can be large and should be regenerated using the pipeline. Small output tables and figures help reviewers quickly understand the results.

### Trade-off

Reviewers need to download the raw dataset and run the pipeline to regenerate all local data artifacts.
