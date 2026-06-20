import subprocess
import sys
from pathlib import Path


PIPELINE_STEPS = [
    ("Extract / raw file validation", "src/extract.py"),
    ("Data profiling", "src/profile_data.py"),
    ("Data transformation", "src/transform.py"),
    ("DuckDB loading and dimensional model", "src/load.py"),
    ("Data quality checks", "src/quality_checks.py"),
    ("SQL market analysis", "src/run_analysis.py"),
    ("EDA visual generation", "src/generate_visuals.py"),
    ("Statistical analysis", "src/statistical_analysis.py"),
]


def run_step(step_name: str, script_path: str) -> None:
    print("\n" + "=" * 80)
    print(f"Running step: {step_name}")
    print(f"Script: {script_path}")
    print("=" * 80)

    if not Path(script_path).exists():
        raise FileNotFoundError(f"Missing pipeline script: {script_path}")

    result = subprocess.run(
        [sys.executable, script_path],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at step: {step_name}")

    print(f"Completed step: {step_name}")


def main():
    print("Starting Inside Airbnb Data Engineering Pipeline")

    for step_name, script_path in PIPELINE_STEPS:
        run_step(step_name, script_path)

    print("\n" + "=" * 80)
    print("Pipeline completed successfully.")
    print("Review outputs in:")
    print("- outputs/tables")
    print("- outputs/tables/analysis")
    print("- outputs/tables/statistics")
    print("- outputs/figures")
    print("=" * 80)


if __name__ == "__main__":
    main()