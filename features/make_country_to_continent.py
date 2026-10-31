
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "country-codes.csv"
)


def make_country_to_continent(df):
    """Create a country-to-continent mapping."""

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    required_columns = [
        "official_name_en",
        "ISO3166-1-Alpha-3",
        "Continent"
    ]

    # Check whether required columns exist
    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df[required_columns] = df[required_columns].replace(
    r"^\s*$",
    pd.NA,
    regex=True
    )

    # Select required columns
    mapping = (
        df[required_columns]
        .dropna(
            subset=[
                "official_name_en",
                "ISO3166-1-Alpha-3"
            ]
        )
        .drop_duplicates()
        .rename(
            columns={
                "official_name_en": "Country_Name",
                "ISO3166-1-Alpha-3": "ISO3",
                "Continent": "Continent_Code"
            }
        )
        .reset_index(drop=True)
    )

    # Fill missing continent codes for North America
    north_america_iso3 = [
        "AIA", "ATG", "ABW", "BHS", "BRB",
        "BLZ", "BMU", "BES", "VGB", "CAN",
        "CYM", "CRI", "CUB", "CUW", "DMA",
        "DOM", "SLV", "GRL", "GRD", "GLP",
        "GTM", "HTI", "HND", "JAM", "MTQ",
        "MEX", "MSR", "NIC", "PAN", "PRI",
        "BLM", "KNA", "LCA", "MAF", "SPM",
        "VCT", "SXM", "TTO", "TCA",
        "USA", "VIR"
    ]

    mapping.loc[
        mapping["ISO3"].isin(north_america_iso3)
        & mapping["Continent_Code"].isna(),
        "Continent_Code"
    ] = "NA"

    return mapping


if __name__ == "__main__":

    df = pd.read_csv(INPUT_FILE,keep_default_na=False)

    country_continent = make_country_to_continent(df)

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "country_to_continent.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save mapping CSV
    country_continent.to_csv(
        output_file,
        index=False
    )

    print("Country-to-continent mapping created!")

    print("\nFirst 10 records:")
    print(country_continent.head(10))

    print("\nTotal countries:", len(country_continent))

    print(
        "Missing continent values:",
        country_continent["Continent_Code"].isna().sum()
    )

    print("\nSaved at:", output_file)

    # Verify saved CSV file
    saved_df = pd.read_csv(output_file, keep_default_na=False)

    print("\n--- Saved CSV Verification ---")
    print("File path:", output_file.resolve())
    print("Total records:", len(saved_df))

    print(
        "Missing continent values:",
        saved_df["Continent_Code"].isna().sum()
    )

    print(
        saved_df[
            saved_df["ISO3"].isin(
                ["AIA", "ATG", "CAN", "MEX", "USA", "VIR"]
            )
        ].to_string(index=False)
    )
