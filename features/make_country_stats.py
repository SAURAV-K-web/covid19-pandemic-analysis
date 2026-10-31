
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "country_cases.csv"
)


def make_country_stats(df):
    """Calculate basic statistics for each country."""

    country_stats = df.copy()

    country_stats["Active_Calculated"] = (
        country_stats["Confirmed"]
        - country_stats["Deaths"]
        - country_stats["Recovered"]
    )

    country_stats["Mortality_Rate"] = (
        country_stats["Deaths"]
        .div(country_stats["Confirmed"].where(
            country_stats["Confirmed"] != 0
        ))
        .mul(100)
    )

    return country_stats


if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE)
    country_stats = make_country_stats(df)

    output_file = (
        PROJECT_ROOT / "data" / "processed" / "country_stats.csv"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    country_stats.to_csv(output_file, index=False)

    print("Country statistics created successfully!")
    print(country_stats.head(10))
    print("Saved at:", output_file)
