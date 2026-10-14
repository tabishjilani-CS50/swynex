import argparse
import json
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def clean_column_name(name):
    return (
        str(name).strip().lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def process_csv(input_file, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_file)
    original_shape = df.shape

    # Standardize column names.
    df.columns = [clean_column_name(c) for c in df.columns]

    # Remove exact duplicate rows.
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # Fill missing numeric values with the median.
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    missing_before = df.isna().sum().to_dict()

    for column in numeric_columns:
        if df[column].isna().any():
            df[column] = df[column].fillna(df[column].median())

    # Fill missing text values with "Unknown".
    categorical_columns = df.select_dtypes(include=["object", "string"]).columns.tolist()
    for column in categorical_columns:
        if df[column].isna().any():
            df[column] = df[column].fillna("Unknown")

    missing_after = df.isna().sum().to_dict()

    # Summary statistics.
    numeric_summary = df[numeric_columns].describe().round(3).to_dict() if numeric_columns else {}

    report = {
        "dataset": Path(input_file).name,
        "original_rows": original_shape[0],
        "original_columns": original_shape[1],
        "final_rows": len(df),
        "final_columns": len(df.columns),
        "duplicates_removed": duplicates,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "missing_values_before": missing_before,
        "missing_values_after": missing_after,
        "numeric_summary": numeric_summary,
    }

    output_csv = output_dir / f"{Path(input_file).stem}_cleaned.csv"
    output_json = output_dir / f"{Path(input_file).stem}_report.json"

    df.to_csv(output_csv, index=False)
    output_json.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    logging.info("Processed %s", input_file)
    logging.info("Saved cleaned dataset: %s", output_csv)
    logging.info("Saved report: %s", output_json)


def main():
    parser = argparse.ArgumentParser(
        description="AutoDataCheck - automated CSV cleaning and dataset reporting."
    )
    parser.add_argument("--input", required=True, help="Path to a CSV file.")
    parser.add_argument(
        "--output",
        default="output",
        help="Directory where cleaned data and reports are saved.",
    )
    args = parser.parse_args()

    process_csv(args.input, args.output)


if __name__ == "__main__":
    main()
