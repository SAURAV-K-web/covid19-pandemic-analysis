 
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_daily_change.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "visualizations"
    / "india_daily_cases_trend.png"
)


def plot_daily_cases_trend():
    """Plot India's daily confirmed COVID-19 cases over time."""

    df = pd.read_csv(INPUT_FILE)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Filter data for India
    india_data = df[df["Country_Region"] == "India"].copy()

    # Sort data by date
    india_data = india_data.sort_values("Date")

    # Remove missing daily change values
    india_data = india_data.dropna(
        subset=["Daily_Confirmed_Change"]
    )

    # Create line chart
    plt.figure(figsize=(12, 6))

    plt.plot(
        india_data["Date"],
        india_data["Daily_Confirmed_Change"],
        marker="o",
        markersize=2,
        linewidth=1
    )

    plt.title("Daily COVID-19 Confirmed Cases in India")
    plt.xlabel("Date")
    plt.ylabel("Daily Confirmed Cases")

    # Format date labels
    ax = plt.gca()

    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b %d, %Y")
    )

    plt.xticks(rotation=45, ha="right")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save chart
    plt.savefig(OUTPUT_FILE, dpi=300)

    plt.show()

    print(f"Chart saved at: {OUTPUT_FILE}")


if __name__ == "__main__":
    plot_daily_cases_trend()
