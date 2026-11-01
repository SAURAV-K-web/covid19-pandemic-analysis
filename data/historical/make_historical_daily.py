from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "historical"
    / "time_series_confirmed.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "historical"
    / "country_historical_daily.csv"
)


def make_historical_daily():
    df = pd.read_csv(INPUT_FILE)

    # Identify date columns
    date_columns = df.columns[4:]

    # Aggregate province-level rows by country
    country_data = df.groupby(
        "Country/Region",
        as_index=False
    )[date_columns].sum()

    # Convert wide format to long format
    daily_data = country_data.melt(
        id_vars=["Country/Region"],
        value_vars=date_columns,
        var_name="Date",
        value_name="Confirmed"
    )

    # Convert date strings to datetime
    daily_data["Date"] = pd.to_datetime(
        daily_data["Date"],
        format="mixed"
    )

    # Sort by country and date
    daily_data = daily_data.sort_values(
        ["Country/Region", "Date"]
    )

    # Calculate daily changes
    daily_data["Daily_Confirmed_Change"] = (
        daily_data.groupby("Country/Region")["Confirmed"]
        .diff()
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    daily_data.to_csv(OUTPUT_FILE, index=False)

    print("Historical daily data created!")
    print("Shape:", daily_data.shape)
    print("Saved at:", OUTPUT_FILE)
    print(daily_data.head())


if __name__ == "__main__":
    make_historical_daily()