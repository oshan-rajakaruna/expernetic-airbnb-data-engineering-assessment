from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("outputs/tables")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


EXPECTED_FILES = [
    "listings.csv.gz",
    "calendar.csv.gz",
    "reviews.csv.gz",
    "neighbourhoods.csv",
    "neighbourhoods.geojson",
]


def file_size_mb(file_path: Path) -> float:
    return round(file_path.stat().st_size / (1024 * 1024), 2)


def main():
    manifest_rows = []

    for filename in EXPECTED_FILES:
        file_path = RAW_DIR / filename
        exists = file_path.exists()

        manifest_rows.append({
            "file_name": filename,
            "relative_path": str(file_path),
            "exists": exists,
            "file_size_mb": file_size_mb(file_path) if exists else None,
            "status": "available" if exists else "missing",
        })

    manifest = pd.DataFrame(manifest_rows)
    output_path = OUTPUT_DIR / "raw_file_manifest.csv"
    manifest.to_csv(output_path, index=False)

    missing_files = manifest[manifest["exists"] == False]

    print("Raw file extraction/validation manifest created.")
    print(f"Saved: {output_path}")

    if not missing_files.empty:
        print("\nMissing required files:")
        print(missing_files[["file_name", "status"]])
        raise FileNotFoundError("One or more required raw files are missing.")

    print("\nAll expected raw files are available.")
    print(manifest)


if __name__ == "__main__":
    main()