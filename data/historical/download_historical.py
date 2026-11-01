from pathlib import Path
from urllib.request import urlretrieve

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "data" / "historical"

URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/archived_data/archived_time_series/time_series_2019-ncov-Confirmed.csv"

OUTPUT_FILE = OUTPUT_DIR / "time_series_confirmed.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

urlretrieve(URL, OUTPUT_FILE)

print("Historical data downloaded successfully!")
print("Saved at:", OUTPUT_FILE)