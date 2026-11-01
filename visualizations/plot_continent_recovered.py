
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
    / "continent_recovered.png"
)


def plot_continent_recovered():
    """Create a bar chart of COVID-19 recovered cases by continent."""

    df = pd.read_csv(INPUT_FILE)

    # Remove rows with missing continent codes
    df = df.dropna(subset=["Continent_Code"])

    # Group recovered cases by continent
    continent_recovered = (
        df.groupby("Continent_Code", as_index=False)
        .agg(Recovered=("Recovered", "sum"))
        .sort_values("Recovered", ascending=False)
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

    continent_recovered["Continent"] = (
        continent_recovered["Continent_Code"].map(continent_names)
    )

    # Create bar chart
    plt.figure(figsize=(10, 6))

    bars = plt.bar(
        continent_recovered["Continent"],
        continent_recovered["Recovered"]
    )

    # Add recovered counts above bars
    plt.bar_label(
        bars,
        fmt="%.0f",
        padding=3,
        fontsize=8
    )

    plt.title("COVID-19 Recovered Cases by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Recovered Cases")

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Save chart
    plt.savefig(OUTPUT_FILE, dpi=300)

    plt.show()

    print(f"Chart saved at: {OUTPUT_FILE}")


if __name__ == "__main__":
    plot_continent_recovered()

