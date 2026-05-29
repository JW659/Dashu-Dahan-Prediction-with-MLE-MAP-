# Dashu-Dahan-Prediction-with-MLE-MAP-
Part of the mini-project for course: fundamentals of machine intelligence 


Predict the hottest (Dashu) and coldest (Dahan) periods in Beijing (2026) by combining 30 years of meteorological data with traditional Chinese 24 Solar Terms, using Maximum Likelihood Estimation (MLE) and Maximum A Posteriori (MAP).

## Overview

- Extracted the central dates of the hottest/coldest 15‑day intervals from Beijing weather data (1994–2023).
- MLE provides a purely data‑driven baseline (normal distribution assumption).
- MAP incorporates the 2026 Solar Term dates as prior knowledge, with tunable prior weights.

## Results

| Method | Dashu (hottest) | Dahan (coldest) |
|--------|----------------|------------------|
| MLE | July 20 | January 7 |
| MAP (σ_prior=7) | July 28 | January 23 |
| MAP (σ_prior=σ_data) | July 24 | January 16 |

## Files

- `MLE.py` – main Python script for data processing, MLE/MAP estimation, and visualization.
- `beijing_weather_30yr.csv` – historical daily temperature data (not included, add your own).
- `Report_MLE_MAP(1).docx` – full project report.
- `beijing_weather_30yr.csv`-Data used

## Usage

1. Place your weather CSV file (columns: `date`, `temp_avg`) in the same directory.
2. Run the script:
   ```bash
   python MLE.py
