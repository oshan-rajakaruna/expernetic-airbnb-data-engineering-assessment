# AI Usage Disclosure

## Project: Inside Airbnb Market Intelligence Data Engineering Pipeline

This document explains how AI tools were used during this project and how all AI-assisted outputs were reviewed, modified, and validated.

---

## AI Tools Used

### ChatGPT

ChatGPT was used as a support tool during the assignment for:

* Breaking down the assignment scope into a practical implementation plan.
* Clarifying data engineering concepts and project structure.
* Reviewing possible approaches for data profiling, cleaning, quality checks, SQL analysis, and statistical testing.
* Drafting initial documentation structures.
* Improving the clarity of technical explanations and business interpretations.

AI was not used as an automated execution system. All code was run locally, reviewed manually, and adjusted based on actual dataset behavior and generated outputs.

---

## AI-Assisted Areas

AI assistance was used in the following areas:

### 1. Project Planning

AI helped organize the broad assignment into a focused scope centered on:

* Dataset familiarization
* Data profiling
* Data cleaning and transformation
* DuckDB analytical modeling
* SQL-based analysis
* Data quality checks
* EDA visualizations
* Statistical testing
* Documentation

### 2. Code Structure Review

AI was used to discuss and review the structure of Python scripts such as:

* `extract.py`
* `profile_data.py`
* `transform.py`
* `load.py`
* `quality_checks.py`
* `run_analysis.py`
* `generate_visuals.py`
* `statistical_analysis.py`
* `main.py`

The scripts were executed locally and adjusted based on actual results, errors, and dataset characteristics.

### 3. Documentation Support

AI was used to help structure and refine:

* README content
* Engineering decision log
* AI usage disclosure
* Business interpretation wording
* Interview-style explanations

Final documentation was reviewed and edited to reflect the actual work completed.

---

## Human Validation

All outputs were manually validated through the following steps:

* Created and activated a local Python virtual environment.
* Installed and verified project dependencies.
* Ran each pipeline script individually.
* Ran the full pipeline using `python main.py`.
* Verified dataset row counts after profiling.
* Reviewed generated cleaned datasets and summary tables.
* Confirmed DuckDB tables were created successfully.
* Reviewed SQL output tables.
* Checked generated visualizations.
* Reviewed statistical test outputs.
* Documented known data limitations, especially missing calendar-level prices.

---

## Important Adjustments Made

Several decisions were made after reviewing the actual dataset and pipeline outputs:

* Calendar-level price analysis was excluded because calendar price values were unavailable.
* Calendar data was used only for availability and occupancy proxy calculations.
* Occupancy was described as a proxy, not confirmed booking occupancy.
* Multi-city analysis was de-scoped to prioritize depth and quality.
* Machine learning and LLM/RAG experiments were de-scoped because the project focused on core data engineering and analytical quality.
* Heavy Jupyter installation was avoided after environment setup issues, and a lighter VS Code-compatible setup was used instead.

---

## Representative Prompts Used

The following are examples of the types of prompts used:

1. Help me break down this Data Engineer Intern assignment into a practical project plan.
2. Explain the Inside Airbnb dataset files and how they relate to each other.
3. Suggest a clean repository structure for a reproducible data engineering project.
4. Review my approach for data profiling, cleaning, and quality checks.
5. Help me explain the business meaning of SQL and statistical results.
6. Help me write a clear decision log and AI usage disclosure.

---

## Final Responsibility Statement

AI was used as a support and review tool. The final project decisions, code execution, output validation, interpretation of results, and submission materials were reviewed and accepted by the candidate.
