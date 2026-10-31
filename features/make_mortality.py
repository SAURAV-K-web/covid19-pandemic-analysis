from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "covid_with_continents.csv"
)


def make_mortality(df):
    """Calculate COVID-19 statistics for each country."""

    df = df.copy()

    # Group data by country and continent
    country_stats = (
        df.groupby(
            ["Country_Region", "Continent_Code"],
            as_index=False
        )
        .agg(
            Confirmed=("Confirmed", "sum"),
            Deaths=("Deaths", "sum"),
            Recovered=("Recovered", "sum"),
            Active=("Active", "sum")
        )
    )

    # Calculate mortality rate
    country_stats["Mortality_Rate"] = (
        country_stats["Deaths"]
        / country_stats["Confirmed"].replace(0, pd.NA)
    ) * 100

    # Calculate recovery rate
    country_stats["Recovery_Rate"] = (
        country_stats["Recovered"]
        / country_stats["Confirmed"].replace(0, pd.NA)
    ) * 100

    # Replace missing rates with zero
    country_stats[
        ["Mortality_Rate", "Recovery_Rate"]
    ] = country_stats[
        ["Mortality_Rate", "Recovery_Rate"]
    ].fillna(0)

    # Sort by confirmed cases
    country_stats = country_stats.sort_values(
        "Confirmed",
        ascending=False
    )

    return country_stats


if __name__ == "__main__":

    # Load COVID-19 data
    df = pd.read_csv(
        INPUT_FILE,
        keep_default_na=False
    )

    # Convert numeric columns
    numeric_columns = [
        "Confirmed",
        "Deaths",
        "Recovered",
        "Active"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    # Generate country statistics
    stats = make_mortality(df)

    # Save processed data
    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "country_stats.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    stats.to_csv(
        output_file,
        index=False
    )

    print("Country mortality analysis completed!")

    print("\nTop 10 countries by confirmed cases:")
    print(stats.head(10).to_string(index=False))

    print("\nTotal countries:", len(stats))

    print("\nSaved at:", output_file)