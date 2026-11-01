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
    / "historical_new_cases_trend.png"
)

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

# Normalize timestamps to calendar dates
df["Date"] = df["Date"].dt.normalize()

# Combine records by country and date
daily_data = (
    df.groupby(["Country/Region", "Date"], as_index=False)
    .agg(
        Confirmed=("Confirmed", "max")
    )
)

# Recalculate daily new cases after grouping
daily_data = daily_data.sort_values(
    ["Country/Region", "Date"]
)

daily_data["Daily_New_Cases"] = (
    daily_data.groupby("Country/Region")["Confirmed"]
    .diff()
)

# Select top 5 countries by latest cumulative cases
latest_date = daily_data["Date"].max()

latest_data = daily_data[
    daily_data["Date"] == latest_date
]

latest_data = latest_data[
    ~latest_data["Country/Region"].isin(["Others"])
]

top_5 = (
    latest_data
    .sort_values("Confirmed", ascending=False)
    .head(5)["Country/Region"]
    .tolist()
)

# Plot daily new cases
plt.figure(figsize=(12, 6))

for country in top_5:
    country_data = daily_data[
        daily_data["Country/Region"] == country
    ].sort_values("Date")

    plt.plot(
        country_data["Date"],
        country_data["Daily_New_Cases"],
        marker="o",
        markersize=3,
        label=country
    )

plt.title("Daily New Confirmed COVID-19 Cases — Top 5 Countries")
plt.xlabel("Date")
plt.ylabel("Daily New Confirmed Cases")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()