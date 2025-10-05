import os
import pandas as pd
from typing import Dict, Any, List, Tuple

def is_schema_file(filename: str) -> bool:
    """Check if the file is a schema file."""
    name = str(filename).lower()
    return '_schema' in name or 'schema' in name

def process_schema_file(file_path: str, folder: str) -> Dict[str, Any]:
    """
    Process a schema file and return its contents in the requested format.
    
    Args:
        file_path: Path to the schema file
        folder: Source or target folder identifier (e.g., 'Bank1', 'Bank2')
        
    Returns:
        dict: Dictionary containing schema information in the requested format
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, header=None)
        
        # Find the header row (contains 'name' or 'description')
        header_row = 0
        for idx, row in df.iterrows():
            if any(isinstance(cell, str) and any(term in str(cell).lower() 
                   for term in ['name', 'description', 'field', 'column']) for cell in row):
                header_row = idx
                break
        
        # Read with the found header row and drop null rows
        df = pd.read_excel(file_path, header=header_row)
        df = df.dropna(how='all')  # Drop completely empty rows
        
        # Clean column names and data
        df = df.rename(columns=lambda x: str(x).strip() if isinstance(x, str) else x)
        
        # Find name and description columns
        name_col = next((col for col in df.columns 
                        if any(term in str(col).lower() 
                        for term in ['name', 'field', 'column'])), None)
        
        desc_col = next((col for col in df.columns 
                        if any(term in str(col).lower() 
                        for term in ['desc', 'definition', 'description'])), None)
        
        # Default to first two columns if not found
        if name_col is None and len(df.columns) > 0:
            name_col = df.columns[0]
        if desc_col is None and len(df.columns) > 1:
            desc_col = df.columns[1]
        
        # Process rows into a list of (name, description) tuples
        fields = []
        
        for _, row in df.iterrows():
            name = str(row.get(name_col, '')).strip()
            desc = str(row.get(desc_col, '')).strip() if desc_col else ''
            
            # Skip empty names and null values
            if not name or name.lower() == 'nan':
                continue
                
            fields.append({'name': name, 'description': desc})
        
        return {
            'file': os.path.basename(file_path),
            'database': folder,
            'type': 'schema',
            'fields': fields
        }
        
    except Exception as e:
        print(f"Error processing schema file {file_path}: {str(e)}")
        return {
            'file': os.path.basename(file_path) if file_path else 'unknown',
            'folder': folder,
            'type': 'schema',
            'error': str(e),
            'fields': []
        }

def process_data_file(file_path: str, folder: str) -> Dict[str, Any]:
    """
    Process a non-schema data file and return its structure.
    
    Args:
        file_path: Path to the data file
        folder: Source or target folder identifier
        
    Returns:
        dict: Dictionary containing file structure information
    """
    try:
        # Read just the headers to get the structure
        if str(file_path).lower().endswith('.csv'):
            df = pd.read_csv(file_path, nrows=0)
        else:  # Excel
            df = pd.read_excel(file_path, nrows=0)
        
        # Extract table name from filename
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        
        return {
            'file': os.path.basename(file_path),
            'database': folder,
            'table': table_name,
            'type': 'data',
            'headers': [str(col).strip() for col in df.columns]
        }
        
    except Exception as e:
        print(f"Error processing data file {file_path}: {str(e)}")
        return {
            'file': os.path.basename(file_path) if file_path else 'unknown',
            'database': folder,
            'type': 'data',
            'error': str(e),
            'headers': []
        }

def process_directory(directory: str, source_type: str = 'source') -> Dict[str, Any]:
    """
    Process all files in a directory and return data in the requested format.
    
    Args:
        directory: Path to the directory to process
        source_type: Type of the source ('source' or 'target')
        
    Returns:
        dict: Dictionary containing processed files in the requested format
    """
    if not os.path.isdir(directory):
        return {'error': f'Directory not found: {directory}'}
    
    # Get database name from directory
    database_name = os.path.basename(directory)
    
    # Get all files and separate schema files
    all_files = []
    schema_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_schema_file(file):
                schema_files.append(file_path)
            elif file.lower().endswith(('.xlsx', '.xls', '.csv')):
                all_files.append(file_path)
    
    # Process schema files first
    schemas = []
    for file_path in sorted(schema_files):
        try:
            schema = process_schema_file(file_path, database_name)
            schemas.append(schema)
        except Exception as e:
            print(f"Error processing schema file {file_path}: {str(e)}")
    
    # Process data files
    tables = []
    for file_path in sorted(all_files):
        try:
            data_file = process_data_file(file_path, database_name)
            
            # Create table entry in the requested format
            table_entry = {
                'TableName': data_file['table'],
                'database': database_name,
                'type': source_type,
                'fields': data_file['headers']
            }
            tables.append(table_entry)
        except Exception as e:
            print(f"Skipping file {file_path} due to error: {str(e)}")
    
    # Extract metadata fields from schemas
    database_metadata = {}
    for schema in schemas:
        for field in schema.get('fields', []):
            field_name = field['name']
            description = field['description']
            
            # Map specific fields to their descriptions
            if 'legalissuecountry' in field_name.lower():
                database_metadata['legalIssueCountry'] = description
            elif 'language' in field_name.lower():
                database_metadata['language'] = description
            elif 'dateofbirth' in field_name.lower() or 'birthdate' in field_name.lower():
                database_metadata['dateOfBirth'] = description
            else:
                database_metadata[field_name] = description
    
    # Format the results in the requested structure
    result = {
        'database': database_name,
        'type': source_type,
        'database_metadata': {
            **database_metadata,
            'Tables': tables
        }
    }
    
    return result
