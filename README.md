# AutoDataCheck

AutoDataCheck is a Python automation tool that processes a CSV dataset, performs common data-cleaning tasks, and generates an automatic dataset-health report.

## What it automates

1. Loads a CSV dataset.
2. Standardizes column names.
3. Detects and removes duplicate rows.
4. Detects missing values.
5. Fills missing numeric values with the column median.
6. Fills missing text values with `Unknown`.
7. Calculates basic numerical statistics.
8. Exports a cleaned CSV.
9. Generates a JSON report describing the transformation.

## Project structure

```text
AutoDataCheck/
├── automate.py
├── requirements.txt
├── README.md
├── sample_data/
│   └── sales.csv
└── output/
```

## Installation

Create a virtual environment if desired:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run it

```bash
python automate.py --input sample_data/sales.csv --output output
```

The program creates:

```text
output/
├── sales_cleaned.csv
└── sales_report.json
```

## Example workflow

Input:

```text
sales.csv
```

Automation:

```text
CSV
 ↓
Load with pandas
 ↓
Standardize columns
 ↓
Detect missing values
 ↓
Remove duplicates
 ↓
Impute missing values
 ↓
Generate statistics
 ↓
Export cleaned CSV + JSON report
```

## Why this is useful

Real machine-learning workflows depend heavily on reliable data preprocessing. This project demonstrates Python automation, pandas, data cleaning, validation, reporting, command-line interfaces, and reproducible data processing.

## Future improvements

- Add HTML/PDF reports.
- Add automatic charts.
- Add outlier detection.
- Add batch processing for an entire folder.
- Add configurable cleaning rules.
- Add unit tests.
