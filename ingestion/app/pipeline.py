from pathlib import Path

from cleaning.functions import (
    clean_data,
    handle_missing_values,
    map_schema,
    remove_duplicates,
    save_processed_data,
    validate_data,
)
from readers.csvReader import read_csv


APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "synthetic_pdo_data_2025.csv"
OUTPUT_PATH = APP_DIR / "data" / "processed" / "synthetic_pdo_data_2025.csv"


def run_pipeline(input_path: Path = DATA_PATH, output_path: Path = OUTPUT_PATH):

    # Step 1: Read data
    df = read_csv(input_path)

    # Step 2: Inspect data
    print("\nColumns:")

    print("\nData types:")



    # Step 3: Remove duplicates
    df = remove_duplicates(df)

    # Step 4: Handle missing values
    df = handle_missing_values(df)

    # Step 5: Validate data
    df = validate_data(df)

    # Step 6: Clean data
    df = clean_data(df)

    # Step 7: Map schema
    df = map_schema(df)

    columns = df.columns.tolist()
    data_types = df.dtypes
    total_count = len(df)

    data = {
        "columns": str(columns),
        "data_types": str(data_types),
        "total_count": str(total_count)
    }

    # Step 8: Save processed data
    save_processed_data(df, output_path)

    return data, output_path

