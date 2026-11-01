
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_cases.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "visualizations"
    / "top_10_country_recovered.png"
)


def plot_top_10_country_recovered():
    """Create a bar chart of the top 10 countries by recovered cases."""

    df = pd.read_csv(INPUT_FILE)

    # Select top 10 countries by recovered cases
    top_10 = (
        df.sort_values("Recovered", ascending=False)
        .head(10)
    )

    # Create bar chart
    plt.figure(figsize=(12, 6))

    bars = plt.bar(
        top_10["Country_Region"],
        top_10["Recovered"]
    )

    # Add recovered counts above bars
    plt.bar_label(
        bars,
        fmt="%.0f",
        padding=3,
        fontsize=8
    )

    plt.title("Top 10 Countries by COVID-19 Recovered Cases")
    plt.xlabel("Country")
    plt.ylabel("Recovered Cases")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save chart
    plt.savefig(OUTPUT_FILE, dpi=300)

    plt.show()

    print(f"Chart saved at: {OUTPUT_FILE}")


if __name__ == "__main__":
    plot_top_10_country_recovered()
