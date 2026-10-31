
from pathlib import Path
import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw data directory
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def load_daily_data():
    """Load and combine daily COVID-19 reports."""

    files = sorted(RAW_DIR.glob("*.csv"))

    daily_data = []

    for file in files:
        df = pd.read_csv(file)

        # Extract date from filename
        df["Date"] = pd.to_datetime(
            file.stem,
            format="%m-%d-%Y"
        )

        daily_data.append(df)

    combined_df = pd.concat(daily_data, ignore_index=True)

    return combined_df



def make_daily_change(df):
    """Calculate daily changes in confirmed COVID-19 cases."""

    country_daily = (
        df.groupby(
            ["Date", "Country_Region"],
            as_index=False
        )
        .agg(
            Confirmed=("Confirmed", "sum")
        )
    )

    country_daily = country_daily.sort_values(
        ["Country_Region", "Date"]
    )

    country_daily["Daily_Confirmed_Change"] = (
        country_daily.groupby("Country_Region")["Confirmed"]
        .diff()
    )

    return country_daily




if __name__ == "__main__":
    df = load_daily_data()

    country_daily = make_daily_change(df)

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "country_daily_change.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    country_daily.to_csv(
        output_file,
        index=False
    )

    print("Daily change data saved successfully!")
    print(country_daily.head(10))
    print("Saved at:", output_file)
