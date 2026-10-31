 
# COVID-19 Pandemic Analysis

## Project Overview

This project analyzes COVID-19 data using Python and Pandas. It processes daily reports, aggregates cases by country, calculates daily changes, and adds geographical information for analysis.

## Objectives

- Analyze confirmed cases, deaths, and recoveries.
- Aggregate COVID-19 data at country level.
- Calculate daily changes in confirmed cases.
- Calculate cases since the first available date.
- Map countries to continents.
- Calculate mortality and recovery rates.
- Extract geographical coordinates.

## Technologies Used

- Python
- Pandas

## Project Workflow

The project processes raw COVID-19 daily reports and generates multiple processed datasets for further analysis.

## Data Processing

1. Load raw COVID-19 daily reports.
2. Aggregate confirmed cases, deaths, and recoveries by country.
3. Calculate daily changes in confirmed cases.
4. Calculate cases since the first available date.
5. Create a country-to-continent mapping.
6. Add continent information to COVID-19 records.
7. Extract geographical coordinates.
8. Calculate country-level statistics and mortality/recovery rates.
9. Save processed datasets in `data/processed/`.

## Generated Datasets

- `country_cases.csv`
- `country_daily_change.csv`
- `country_cases_since_t0.csv`
- `country_to_continent.csv`
- `covid_with_continents.csv`
- `country_coordinates.csv`
- `country_stats.csv`
- `country_mortality.csv`
- `unmatched_countries.csv`

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SAURAV-K-web/covid19-pandemic-analysis.git
cd covid19-pandemic-analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment (Windows)

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the feature pipeline

```bash
python features/make_all.py
```

Processed CSV files will be generated in `data/processed/`.

## Data Quality Notes

Some records represent cruise ships or event-related entries rather than countries. These records are preserved and listed in `unmatched_countries.csv`.

The first available date has no previous date for comparison, so daily-change calculations may contain missing values.


## Conclusion

This project demonstrates how Python and Pandas can be used to process and analyze COVID-19 data. Daily reports are transformed into country-level datasets, daily case changes are calculated, and geographical information is added through continent mapping and coordinates.

The project also calculates country-level statistics, including mortality and recovery rates. The generated datasets provide a structured foundation for further analysis and data visualization.

Overall, this project helped develop practical skills in data loading, data aggregation, data transformation, and data quality handling using Pandas.

## Author

Saurav Kumar Prasad
