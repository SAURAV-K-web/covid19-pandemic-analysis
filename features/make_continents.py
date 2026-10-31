
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

COVID_FILE = (
    PROJECT_ROOT / "data" / "raw" / "10-05-2020.csv"
)

MAPPING_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_to_continent.csv"
)


def make_continents(covid_df, mapping_df):
    """Add continent information to COVID-19 data."""

    covid_df = covid_df.copy()
    mapping_df = mapping_df.copy()

    # Clean country names
    covid_df["Country_Region"] = (
        covid_df["Country_Region"].str.strip()
    )

    mapping_df["Country_Name"] = (
        mapping_df["Country_Name"].str.strip()
    )

    # Country name aliases
    country_aliases = {
        "Korea, North": "Democratic People's Republic of Korea",
        "Korea, South": "Republic of Korea",
        "US": "United States of America",
        "Taiwan*": "Taiwan",
        "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
        "Venezuela": "Venezuela (Bolivarian Republic of)",
        "Vietnam": "Viet Nam",
        "Tanzania": "United Republic of Tanzania",
        "Bolivia": "Bolivia (Plurinational State of)",
        "Congo (Brazzaville)": "Congo",
        "Congo (Kinshasa)": "Democratic Republic of the Congo",
        "Iran": "Iran (Islamic Republic of)",
        "Russia": "Russian Federation",

        # Additional country aliases
        "Brunei": "Brunei Darussalam",
        "Burma": "Myanmar",
        "Cote d'Ivoire": "Ivory Coast",
        "Laos": "Lao People's Democratic Republic",
        "Moldova": "Republic of Moldova",
        "Syria": "Syrian Arab Republic",
        "Turkey": "Türkiye",
        "West Bank and Gaza": "State of Palestine",
        "Kosovo": "Kosovo"
    }

    # Replace country names
    covid_df["Country_Region"] = (
        covid_df["Country_Region"]
        .replace(country_aliases)
    )

    # Display country names
    print("Updated country names:")
    print(
        covid_df["Country_Region"]
        .drop_duplicates()
        .head(20)
    )

    print("\nMapping country names:")
    print(mapping_df["Country_Name"].head(20))

    # Merge COVID data with continent mapping
    continents = covid_df.merge(
        mapping_df,
        left_on="Country_Region",
        right_on="Country_Name",
        how="left"
    )

    # Manually assign continent to Kosovo
    continents.loc[
        continents["Country_Region"] == "Kosovo",
        "Continent_Code"
    ] = "EU"

    return continents


if __name__ == "__main__":

    covid_df = pd.read_csv(COVID_FILE)

    # Preserve NA as North America
    mapping_df = pd.read_csv(
        MAPPING_FILE,
        keep_default_na=False
    )

    continents = make_continents(
        covid_df,
        mapping_df
    )

    # Save continent-mapped COVID-19 data
    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "covid_with_continents.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    continents.to_csv(
        output_file,
        index=False
    )

    print("\nContinent mapping completed!")

    print(
        continents[
            ["Country_Region", "Country_Name", "Continent_Code"]
        ].head(10)
    )

    # Identify unmatched countries
    unmatched = (
        continents.loc[
            continents["Continent_Code"].isna()
            | continents["Continent_Code"].eq(""),
            ["Country_Region"]
        ]
        .drop_duplicates()
        .sort_values("Country_Region")
    )

    # Save unmatched countries
    unmatched_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "unmatched_countries.csv"
    )

    unmatched.to_csv(
        unmatched_file,
        index=False
    )

    print("\nUnmatched countries:")
    print(unmatched.to_string(index=False))

    print("\nTotal unmatched countries:", len(unmatched))

    print("\nSaved at:", output_file)
    print("Unmatched list saved at:", unmatched_file)
