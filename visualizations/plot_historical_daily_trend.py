from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "historical"
    / "country_historical_daily.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "visualizations"
    / "historical_daily_trend.png"
)

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

# Combine multiple timestamps on the same calendar date
df["Date"] = df["Date"].dt.normalize()

daily_data = (
    df.groupby(["Country/Region", "Date"], as_index=False)
    .agg(
        Confirmed=("Confirmed", "max"),
        Daily_Confirmed_Change=("Daily_Confirmed_Change", "sum")
    )
)

# Select top 5 countries by latest confirmed cases
latest_date = daily_data["Date"].max()

latest_data = daily_data[daily_data["Date"] == latest_date]

top_5 = (
    latest_data
    .sort_values("Confirmed", ascending=False)
    .head(5)["Country/Region"]
    .tolist()
)

plt.figure(figsize=(12, 6))

for country in top_5:
    country_data = daily_data[
        daily_data["Country/Region"] == country
    ].sort_values("Date")

    plt.plot(
        country_data["Date"],
        country_data["Confirmed"],
        marker="o",
        markersize=3,
        label=country
    )

plt.title("Historical Confirmed COVID-19 Cases — Top 5 Countries")
plt.xlabel("Date")
plt.ylabel("Cumulative Confirmed Cases")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()