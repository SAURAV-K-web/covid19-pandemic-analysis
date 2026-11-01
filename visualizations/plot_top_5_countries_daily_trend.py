from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

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
    / "top_5_countries_daily_trend.png"
)

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

# Latest date ke basis par top 5 countries
latest_date = df["Date"].max()

latest_data = df[df["Date"] == latest_date]

top_5_countries = (
    latest_data
    .sort_values("Daily_Confirmed_Change", ascending=False)
    .head(5)["Country_Region"]
    .tolist()
)

# In 5 countries ka complete daily trend
trend_data = df[df["Country_Region"].isin(top_5_countries)]

plt.figure(figsize=(12, 6))

for country in top_5_countries:
    country_data = trend_data[
        trend_data["Country_Region"] == country
    ].sort_values("Date")

    plt.plot(
        country_data["Date"],
        country_data["Daily_Confirmed_Change"],
        label=country
    )

plt.title("Daily Confirmed Cases Trend — Top 5 Countries")
plt.xlabel("Date")
plt.ylabel("Daily Confirmed Cases")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()