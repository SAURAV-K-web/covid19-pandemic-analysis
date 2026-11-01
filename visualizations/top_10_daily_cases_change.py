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
    / "top_10_daily_cases_change.png"
)

df = pd.read_csv(INPUT_FILE)

# Latest date ka data select karo
latest_date = df["Date"].max()

latest_data = df[df["Date"] == latest_date]

# Top 10 countries by daily confirmed cases
top_10 = (
    latest_data
    .sort_values("Daily_Confirmed_Change", ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

bars = plt.bar(
    top_10["Country_Region"],
    top_10["Daily_Confirmed_Change"]
)

plt.bar_label(bars, fmt="%.0f", padding=3)

plt.title(f"Top 10 Countries by Daily Confirmed Cases ({latest_date})")
plt.xlabel("Country")
plt.ylabel("Daily Confirmed Cases")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()