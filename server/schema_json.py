import pandas as pd
import json
import os

def extract_schema_from_dir(dir_path):
    # Find schema files in directory
    schema_files = [f for f in os.listdir(dir_path) if f.endswith("_Schema.xlsx")]

    # If not exactly one schema file, raise unified error
    if len(schema_files) != 1:
        raise ValueError(f"None or more than one '_Schema.xlsx' file found in directory: {dir_path}")

    file_path = os.path.join(dir_path, schema_files[0])
    file_name = os.path.basename(file_path)

    # Read all sheets
    all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)

    database_json = {
        "Database": "Source",
        "filename": file_name,
        "Tables": {}
    }

    for sheet_name, df in all_sheets.items():
        # Drop empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        if df.empty:
            continue

        df = df.reset_index(drop=True)

        # Detect header row (contains 'name' and 'description')
        header_index = None
        for i, row in df.iterrows():
            row_values = [str(v).strip().lower() for v in row if pd.notna(v)]
            if "name" in row_values and "description" in row_values:
                header_index = i
                break

        if header_index is None:
            continue

        # Set header and clean data
        df.columns = df.iloc[header_index]
        df = df.iloc[header_index + 1:].dropna(how='all')
        df.columns = [str(c).strip().lower() for c in df.columns]

        if "name" not in df.columns or "description" not in df.columns:
            continue

        # Build table columns
        table_columns = {}
        for _, row in df.iterrows():
            name = str(row["name"]).strip() if pd.notna(row["name"]) else None
            desc = str(row["description"]).strip() if pd.notna(row["description"]) else ""
            if name:
                table_columns[name] = desc

        if table_columns:
            database_json["Tables"][sheet_name] = {
                "name": sheet_name,
                "Table Columns": table_columns
            }

    return json.dumps(database_json, indent=4, ensure_ascii=False)
