
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def make_coordinates(df):
    """Extract geographical coordinates from COVID-19 data."""

    coordinates = (
        df[["Country_Region", "Lat", "Long_"]]
        .dropna(subset=["Country_Region", "Lat", "Long_"])
        .drop_duplicates()
        .sort_values("Country_Region")
        .reset_index(drop=True)
    )

    return coordinates


def load_data():
    """Load the first daily COVID-19 report."""

    input_file = RAW_DIR / "10-05-2020.csv"
    return pd.read_csv(input_file)


if __name__ == "__main__":
    df = load_data()
    coordinates = make_coordinates(df)

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "country_coordinates.csv"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    coordinates.to_csv(output_file, index=False)

    print("Coordinates data created successfully!")
    print(coordinates.head(10))
    print("Saved at:", output_file)
