from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "Date",
    "Well_ID",
    "Field_Name",
    "Zone",
    "Status",
    "Risk_Level",
}

COLUMN_MAPPING = {
    "Date": "date",
    "Well_ID": "well_id",
    "Field_Name": "field_name",
    "Zone": "zone",
    "Lat": "latitude",
    "Long": "longitude",
    "Well_Age": "well_age",
    "Choke_Size": "choke_size",
    "THP": "tubing_head_pressure",
    "BHP": "bottomhole_pressure",
    "Oil_Rate": "oil_rate",
    "Gas_Rate": "gas_rate",
    "Water_Rate": "water_rate",
    "GOR": "gas_oil_ratio",
    "Water_Cut": "water_cut",
    "Uptime": "uptime",
    "NPT_Event": "npt_event",
    "Status": "status",
    "Drawdown": "drawdown",
    "Efficiency_Index": "efficiency_index",
    "Vibration": "vibration",
    "Integrity_Score": "integrity_score",
    "Risk_Level": "risk_level",
}


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with duplicate records removed."""
    return df.drop_duplicates().reset_index(drop=True)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill numeric gaps with medians and text gaps with a clear placeholder."""
    result = df.copy()
    numeric_columns = result.select_dtypes(include="number").columns
    text_columns = result.select_dtypes(exclude="number").columns

    for column in numeric_columns:
        result[column] = result[column].fillna(result[column].median())
    for column in text_columns:
        result[column] = result[column].fillna("Unknown")

    return result


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate the required structure and return the unchanged DataFrame."""
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")
    if df.empty:
        raise ValueError("Input data contains no rows")
    if df.isnull().any().any():
        raise ValueError("Input data still contains missing values")

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column values and convert the date column to datetime."""
    result = df.copy()
    result.columns = result.columns.str.strip()

    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].astype(str).str.strip()

    if "Date" in result.columns:
        result["Date"] = pd.to_datetime(result["Date"], errors="raise")

    return result


def map_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Map source column names to the platform schema."""
    return df.rename(columns=COLUMN_MAPPING)


def save_processed_data(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Write processed data to CSV and return the path that was written."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    df.to_csv(path, index=False)
    return path