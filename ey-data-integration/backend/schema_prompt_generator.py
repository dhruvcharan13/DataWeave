#!/usr/bin/env python3
"""
Schema Prompt Generator for EY Data Integration Challenge
Generates simple schema prompts for Gemini AI to analyze relationships
"""

import os
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

class SchemaPromptGenerator:
    def __init__(self):
        self.bank1_schema = {}
        self.bank2_schema = {}
    
    def generate_schema_prompts(self):
        """Generate simple schema prompts for both banks"""
        print("Generating schema prompts for Gemini AI...")
        
        # Process Bank 1
        self.bank1_schema = self._process_bank_schema("Bank 1 Data")
        
        # Process Bank 2  
        self.bank2_schema = self._process_bank_schema("Bank 2 Data")
        
        # Generate prompts
        bank1_prompt = self._create_gemini_prompt("Bank 1", self.bank1_schema)
        bank2_prompt = self._create_gemini_prompt("Bank 2", self.bank2_schema)
        
        # Save prompts
        self._save_prompt("bank1_schema_prompt.txt", bank1_prompt)
        self._save_prompt("bank2_schema_prompt.txt", bank2_prompt)
        
        print(f"\n{'='*80}")
        print("SCHEMA PROMPTS GENERATED!")
        print("Bank1 prompt: bank1_schema_prompt.txt")
        print("Bank2 prompt: bank2_schema_prompt.txt")
        print("Send these prompts to Gemini to get relationship analysis")
        print('='*80)
        
        return {
            'bank1_prompt': bank1_prompt,
            'bank2_prompt': bank2_prompt
        }
    
    def _process_bank_schema(self, bank_folder: str) -> Dict:
        """Process a bank folder and extract simple schema info"""
        print(f"\nProcessing {bank_folder}...")
        
        schema_info = {
            'bank_name': bank_folder,
            'tables': []
        }
        
        for file in sorted(os.listdir(bank_folder)):
            file_path = os.path.join(bank_folder, file)
            file_lower = file.lower()
            
            # Skip non-data files
            if not (file_lower.endswith('.csv') or file_lower.endswith(('.xlsx', '.xls'))):
                continue
            if file_lower.startswith('~$'):  # Skip Excel temp files
                continue
                
            table_info = self._extract_table_schema(file_path, bank_folder)
            if table_info:
                schema_info['tables'].append(table_info)
        
        print(f"Found {len(schema_info['tables'])} tables in {bank_folder}")
        return schema_info
    
    def _extract_table_schema(self, file_path: str, bank_folder: str) -> Dict:
        """Extract simple schema info from a data file"""
        file = os.path.basename(file_path)
        table_name = os.path.splitext(file)[0]
        
        try:
            if file.lower().endswith('.csv'):
                # Read only header row from CSV
                with open(file_path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)
            else:
                # Read Excel file (first sheet only)
                df = pd.read_excel(file_path, nrows=0)  # Only headers
                headers = df.columns.tolist()
            
            if not headers:
                return None
                
            return {
                'table_name': table_name,
                'file_name': file,
                'columns': headers,
                'column_count': len(headers)
            }
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return None
    
    def _create_gemini_prompt(self, bank_name: str, schema: Dict) -> str:
        """Create a prompt for Gemini to analyze relationships"""
        prompt = f"""
# {bank_name} Database Schema Analysis

Please analyze the following database schema and identify relationships between tables.

## Database: {bank_name}

### Tables and Columns:

"""
        
        for table in schema['tables']:
            prompt += f"**Table: {table['table_name']}**\n"
            prompt += f"File: {table['file_name']}\n"
            prompt += f"Columns ({table['column_count']}): {', '.join(table['columns'])}\n\n"
        
        prompt += """
## Your Task:

1. **Identify Primary Keys**: For each table, identify which column(s) serve as primary keys
2. **Identify Foreign Keys**: Find columns that reference other tables
3. **Map Relationships**: Create a relationship map showing how tables connect
4. **Suggest Improvements**: Recommend any schema improvements

## Expected Output Format:

Please provide your analysis in the following JSON format:

```json
{
  "bank_name": "{bank_name}",
  "tables": [
    {
      "table_name": "table_name",
      "primary_keys": ["column1", "column2"],
      "foreign_keys": [
        {
          "column": "column_name",
          "references_table": "other_table",
          "references_column": "other_column",
          "relationship_type": "one_to_many|many_to_one|one_to_one"
        }
      ],
      "suggested_improvements": [
        "Add index on column X",
        "Consider normalizing table Y"
      ]
    }
  ],
  "relationships": [
    {
      "parent_table": "table1",
      "child_table": "table2", 
      "parent_column": "id",
      "child_column": "table1_id",
      "relationship_type": "one_to_many",
      "confidence": 0.9
    }
  ],
  "summary": {
    "total_tables": 5,
    "total_relationships": 8,
    "schema_quality_score": 8.5
  }
}
```

Please analyze the schema and provide your response in the exact JSON format above.
"""
        
        return prompt
    
    def _save_prompt(self, filename: str, content: str):
        """Save prompt to file in backend directory"""
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(backend_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved prompt to {filepath}")

def main():
    generator = SchemaPromptGenerator()
    generator.generate_schema_prompts()

if __name__ == "__main__":
    main()
