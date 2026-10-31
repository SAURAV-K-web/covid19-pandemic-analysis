
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def load_daily_data():
    """Load and combine daily COVID-19 reports."""

    files = sorted(RAW_DIR.glob("*.csv"))
    daily_data = []

    for file in files:
        df = pd.read_csv(file)
        df["Date"] = pd.to_datetime(
            file.stem,
            format="%m-%d-%Y"
        )
        daily_data.append(df)

    return pd.concat(daily_data, ignore_index=True)


def make_cases_since_t0(df):
    """Calculate confirmed cases relative to each country's first date."""

    country_daily = (
        df.groupby(
            ["Date", "Country_Region"],
            as_index=False
        )
        .agg(Confirmed=("Confirmed", "sum"))
    )

    country_daily = country_daily.sort_values(
        ["Country_Region", "Date"]
    )

    first_confirmed = (
        country_daily.groupby("Country_Region")["Confirmed"]
        .transform("first")
    )

    country_daily["Confirmed_Since_T0"] = (
        country_daily["Confirmed"] - first_confirmed
    )

    return country_daily


if __name__ == "__main__":
    df = load_daily_data()
    country_t0 = make_cases_since_t0(df)

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "country_cases_since_t0.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    country_t0.to_csv(output_file, index=False)

    print("Cases since t0 created successfully!")
    print(country_t0.head(10))
    print("Saved at:", output_file)
