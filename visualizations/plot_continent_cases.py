
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "covid_with_continents.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "visualizations"
    / "continent_confirmed_cases.png"
)


def plot_continent_cases():
    """Create a bar chart of confirmed cases by continent."""

    df = pd.read_csv(INPUT_FILE)

    # Remove rows with missing continent codes
    df = df.dropna(subset=["Continent_Code"])

    # Group confirmed cases by continent
    continent_cases = (
        df.groupby("Continent_Code", as_index=False)
        .agg(Confirmed=("Confirmed", "sum"))
        .sort_values("Confirmed", ascending=False)
    )

    # Convert continent codes into readable names
    continent_names = {
        "AS": "Asia",
        "EU": "Europe",
        "AF": "Africa",
        "SA": "South America",
        "OC": "Oceania",
        "AN": "Antarctica",
    }

    continent_cases["Continent"] = (
        continent_cases["Continent_Code"].map(continent_names)
    )

    # Create bar chart
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        continent_cases["Continent"],
        continent_cases["Confirmed"]
    )

    # Add case counts above bars
    plt.bar_label(
        bars,
        fmt="%.0f",
        padding=3,
        fontsize=8
    )

    plt.title("Confirmed COVID-19 Cases by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Confirmed Cases")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Save chart
    plt.savefig(OUTPUT_FILE, dpi=300)

    plt.show()

    print(f"Chart saved at: {OUTPUT_FILE}")


if __name__ == "__main__":
    plot_continent_cases()
