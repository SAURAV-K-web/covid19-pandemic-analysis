from pathlib import Path
import pandas as pd

from make_cases import load_data, make_country_cases
from make_cases_daily_change import (
    load_daily_data,
    make_daily_change
)
from make_cases_since_t0 import make_cases_since_t0
from make_continents import make_continents
from make_coordinates import make_coordinates
from make_country_stats import make_country_stats
from make_country_to_continent import make_country_to_continent
from make_mortality import make_mortality


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "10-05-2020.csv"

MAPPING_FILE = (
    PROJECT_ROOT / "data" / "reference" / "country-codes.csv"
)


def main():

    print("\n1. Creating country cases...")
    raw_df = load_data()
    country_cases = make_country_cases(raw_df)

    print("\n2. Creating daily change...")
    daily_df = load_daily_data()
    daily_change = make_daily_change(daily_df)

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "country_daily_change.csv"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    daily_change.to_csv(output_file, index=False)

    print("\n3. Creating cases since t0...")
    cases_since_t0 = make_cases_since_t0(daily_df)

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "country_cases_since_t0.csv"
    )
    cases_since_t0.to_csv(output_file, index=False)

    print("\n4. Creating country-continent mapping...")
    mapping_df = pd.read_csv(
        MAPPING_FILE,
        keep_default_na=False
    )
    country_mapping = make_country_to_continent(mapping_df)

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "country_to_continent.csv"
    )
    country_mapping.to_csv(output_file, index=False)

    print("\n5. Adding continent information...")
    covid_with_continents = make_continents(
        raw_df,
        country_mapping
    )

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "covid_with_continents.csv"
    )
    covid_with_continents.to_csv(output_file, index=False)

    print("\n6. Creating coordinates...")
    coordinates = make_coordinates(raw_df)

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "country_coordinates.csv"
    )
    coordinates.to_csv(output_file, index=False)

    print("\n7. Creating country statistics...")
    country_stats = make_country_stats(country_cases)

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "country_stats.csv"
    )
    country_stats.to_csv(output_file, index=False)

    print("\n8. Creating mortality and recovery rates...")
    mortality = make_mortality(covid_with_continents)

    output_file = (
        PROJECT_ROOT / "data" / "processed"
        / "country_mortality.csv"
    )
    mortality.to_csv(output_file, index=False)

    print("\nAll feature files created successfully!")


if __name__ == "__main__":
    main()