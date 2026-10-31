
from pathlib import Path
import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw COVID-19 dataset
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "10-05-2020.csv"


def load_data():
    """Load the raw COVID-19 dataset."""
    df = pd.read_csv(DATA_FILE)

    print("Dataset loaded successfully!")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    return df


def inspect_country_rows(df):
    """Inspect country-level and province-level records."""

    columns = [
        "Province_State",
        "Country_Region",
        "Confirmed",
        "Deaths",
        "Recovered"
    ]

    # Inspect Afghanistan and China
    for country in ["Afghanistan", "China"]:
        print(f"\n--- {country} ---")

        country_df = df.loc[
            df["Country_Region"] == country,
            columns
        ]

        print(country_df.head(10).to_string(index=False))
        print("Rows:", len(country_df))

    # Show top 10 countries by row count
    print("\n--- Top 10 countries by row count ---")

    country_counts = (
        df.groupby("Country_Region")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    print(country_counts)

    # Check missing values
    print("\n--- Missing values ---")

    columns_to_check = [
        "Province_State",
        "Country_Region",
        "Confirmed",
        "Deaths",
        "Recovered"
    ]

    print(df[columns_to_check].isna().sum())



    print("\n--- Country and province summary ---")

    print(
        df.groupby("Country_Region")
        .agg(
            total_rows=("Country_Region", "size"),
            province_names=("Province_State", "nunique"),
            missing_province=("Province_State", lambda s: s.isna().sum())
        )
        .sort_values("total_rows", ascending=False)
        .head(10)
    )


def make_country_cases(df):
    """Aggregate COVID-19 cases by country."""

    country_cases = (
        df.groupby("Country_Region", as_index=False)
        .agg(
            Confirmed=("Confirmed", "sum"),
            Deaths=("Deaths", "sum"),
            Recovered=("Recovered", "sum")
        )
    )

    output_file = (
        PROJECT_ROOT / "data" / "processed" / "country_cases.csv"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    country_cases.to_csv(output_file, index=False)

    print("\nCountry-level data created successfully!")
    print(country_cases.head(10))
    print("Saved at:", output_file)

    return country_cases


if __name__ == "__main__":
    df = load_data()
    inspect_country_rows(df)
    country_cases = make_country_cases(df)
