
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
    / "continent_deaths.png"
)


def plot_continent_deaths():
    """Create a bar chart of COVID-19 deaths by continent."""

    df = pd.read_csv(INPUT_FILE)

    # Remove rows with missing continent codes
    df = df.dropna(subset=["Continent_Code"])

    # Group deaths by continent
    continent_deaths = (
        df.groupby("Continent_Code", as_index=False)
        .agg(Deaths=("Deaths", "sum"))
        .sort_values("Deaths", ascending=False)
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

    continent_deaths["Continent"] = (
        continent_deaths["Continent_Code"].map(continent_names)
    )

    # Create bar chart
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        continent_deaths["Continent"],
        continent_deaths["Deaths"]
    )

    # Add death counts above bars
    plt.bar_label(
        bars,
        fmt="%.0f",
        padding=3,
        fontsize=8
    )

    plt.title("COVID-19 Deaths by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Deaths")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Save chart
    plt.savefig(OUTPUT_FILE, dpi=300)

    plt.show()

    print(f"Chart saved at: {OUTPUT_FILE}")


if __name__ == "__main__":
    plot_continent_deaths()
