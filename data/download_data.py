
from pathlib import Path
from urllib.request import urlretrieve

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

dates = [
    "10-05-2020",
    "10-06-2020",
    "10-07-2020",
    "10-08-2020",
    "10-09-2020",
    "10-10-2020",
]

base_url = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
    "master/csse_covid_19_data/csse_covid_19_daily_reports/"
)

for date in dates:
    url = f"{base_url}{date}.csv"
    output_file = RAW_DIR / f"{date}.csv"

    if output_file.exists():
        print(f"Already exists: {output_file.name}")
        continue

    try:
        urlretrieve(url, output_file)
        print(f"Downloaded: {output_file.name}")
    except Exception as error:
        print(f"Failed: {date} — {error}")


# Download country and continent reference data
REFERENCE_DIR = DATA_DIR / "reference"
REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

mapping_url = (
    "https://datahub.io/core/country-codes/"
    "_r/-/data/country-codes.csv"
)

mapping_file = REFERENCE_DIR / "country-codes.csv"

if mapping_file.exists():
    print("Already exists:", mapping_file.name)
else:
    try:
        urlretrieve(mapping_url, mapping_file)
        print("Downloaded:", mapping_file.name)
    except Exception as error:
        print("Mapping download failed:", error)
