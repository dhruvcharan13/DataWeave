import os
import csv
import pandas as pd

def read_schema_file(file_path, folder):
    """Read and print the contents of a schema file."""
    print("\n" + "="*80)
    print(f"SCHEMA FILE: {os.path.basename(file_path)}")
    print(f"DATABASE: {folder}")
    print("="*80)
    
    try:
        # Read the entire Excel file
        df = pd.read_excel(file_path, header=None)
        
        # Find the first row that looks like a header (contains 'name' or 'description')
        header_row = 0
        for idx, row in df.iterrows():
            if any(isinstance(cell, str) and any(term in str(cell).lower() for term in ['name', 'description']) for cell in row):
                header_row = idx
                break
        
        # Read the file again with the found header row
        df = pd.read_excel(file_path, header=header_row)
        
        # Clean up the data
        df = df.dropna(how='all')  # Remove completely empty rows
        df = df.rename(columns=lambda x: str(x).strip() if isinstance(x, str) else x)
        
        # Print the schema in a clean format
        print("\nSCHEMA DEFINITION:")
        print("-" * 80)
        
        # Find the name and description columns (case insensitive)
        name_col = None
        desc_col = None
        
        for col in df.columns:
            col_str = str(col).lower()
            if 'name' in col_str or 'field' in col_str:
                name_col = col
            elif 'desc' in col_str or 'definition' in col_str:
                desc_col = col
        
        # Default to first two columns if not found
        if name_col is None and len(df.columns) > 0:
            name_col = df.columns[0]
        if desc_col is None and len(df.columns) > 1:
            desc_col = df.columns[1]
        
        # Print each field with its description
        for _, row in df.iterrows():
            try:
                field = str(row[name_col]).strip() if name_col is not None and pd.notna(row.get(name_col)) else ""
                desc = str(row[desc_col]).strip() if desc_col is not None and pd.notna(row.get(desc_col)) else ""
                
                if field and field.lower() != 'nan' and not any(term in field.lower() for term in ['name', 'description']):
                    print(f"{field:<30} | {desc}")
            except (KeyError, IndexError):
                continue
                
        print("-" * 80)
        
    except Exception as e:
        print(f"Error reading schema file {file_path}: {str(e)}")
        # Print the error with more details
        import traceback
        traceback.print_exc()

def process_other_file(file_path, folder):
    """Process and print only headers of non-schema files."""
    file = os.path.basename(file_path)
    file_lower = file.lower()
    table_name = os.path.splitext(file)[0]
    
    try:
        if file_lower.endswith('.csv'):
            # Read only header row from CSV
            with open(file_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                headers = next(reader, None)  # first row only
        else:
            # Read Excel file (first sheet only)
            xl = pd.ExcelFile(file_path)
            if len(xl.sheet_names) > 0:
                # Read just the first row of the first sheet
                df = pd.read_excel(file_path, nrows=1)
                headers = df.columns.tolist()
            else:
                headers = []
        
        if headers:
            print(f"\nDatabase: {folder}")
            print(f"Table: {table_name}")
            print(f"File: {file}")
            print(f"Headers: {', '.join(headers)}")
            print("-" * 50)
            
    except Exception as e:
        print(f"\nError processing {file_path}: {str(e)}")

def main():
    # Process each bank folder one at a time
    for folder in ["Bank1", "Bank2"]:
        print("\n" + "="*80)
        print(f"PROCESSING: {folder}")
        print("="*80)
        
        # First process the schema file for this bank
        schema_file = os.path.join(folder, f"{folder}_Schema.xlsx")
        if os.path.exists(schema_file):
            read_schema_file(schema_file, folder)
        else:
            print(f"\nNo schema file found for {folder}")
        
        # Then process other files in this bank's folder
        print(f"\n{'*'*40}")
        print(f"FILES IN {folder}:")
        print('*'*40)
        
        for file in sorted(os.listdir(folder)):  # Sort files for consistent order
            file_path = os.path.join(folder, file)
            file_lower = file.lower()
            
            # Skip schema files (already processed) and non-data files
            if file_lower.endswith('_schema.xlsx'):
                continue
            if not (file_lower.endswith('.csv') or file_lower.endswith(('.xlsx', '.xls'))):
                continue
                
            process_other_file(file_path, folder)
            
        print("\n" + "="*80)
        print(f"COMPLETED: {folder}")
        print("="*80)

if __name__ == "__main__":
    main()
