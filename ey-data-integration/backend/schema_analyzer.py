import os
import csv
import pandas as pd
from typing import Dict, List, Any, Tuple
import json

class SchemaAnalyzer:
    """Enhanced schema analyzer for bank data integration"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "/Users/dhruvcharan/Documents/HTVX"
        self.bank_schemas = {}
        self.bank_tables = {}
    
    def read_schema_file(self, file_path: str, folder: str) -> Dict[str, Any]:
        """Read and analyze the contents of a schema file."""
        print(f"\n{'='*80}")
        print(f"SCHEMA FILE: {os.path.basename(file_path)}")
        print(f"DATABASE: {folder}")
        print('='*80)
        
        try:
            # Read the entire Excel file
            df = pd.read_excel(file_path, header=None)
            
            # Find the first row that looks like a header
            header_row = 0
            for idx, row in df.iterrows():
                if any(isinstance(cell, str) and any(term in str(cell).lower() for term in ['name', 'description']) for cell in row):
                    header_row = idx
                    break
            
            # Read the file again with the found header row
            df = pd.read_excel(file_path, header=header_row)
            
            # Clean up the data
            df = df.dropna(how='all')
            df = df.rename(columns=lambda x: str(x).strip() if isinstance(x, str) else x)
            
            # Find the name and description columns
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
            
            # Extract schema information
            schema_fields = []
            for _, row in df.iterrows():
                try:
                    field = str(row[name_col]).strip() if name_col is not None and pd.notna(row.get(name_col)) else ""
                    desc = str(row[desc_col]).strip() if desc_col is not None and pd.notna(row.get(desc_col)) else ""
                    
                    if field and field.lower() != 'nan' and not any(term in field.lower() for term in ['name', 'description']):
                        schema_fields.append({
                            'field_name': field,
                            'description': desc,
                            'data_type': self._infer_data_type(field, desc)
                        })
                except (KeyError, IndexError):
                    continue
            
            schema_info = {
                'database': folder,
                'schema_file': os.path.basename(file_path),
                'fields': schema_fields,
                'field_count': len(schema_fields)
            }
            
            # Print the schema in a clean format
            print(f"\nSCHEMA DEFINITION ({len(schema_fields)} fields):")
            print("-" * 80)
            for field in schema_fields:
                print(f"{field['field_name']:<30} | {field['description']}")
            print("-" * 80)
            
            return schema_info
            
        except Exception as e:
            print(f"Error reading schema file {file_path}: {str(e)}")
            return {'error': str(e)}
    
    def _infer_data_type(self, field_name: str, description: str) -> str:
        """Infer data type from field name and description"""
        field_lower = field_name.lower()
        desc_lower = description.lower()
        
        # ID fields
        if any(term in field_lower for term in ['id', 'key', 'reference']):
            return 'identifier'
        
        # Date fields
        if any(term in field_lower for term in ['date', 'time', 'created', 'updated', 'expired', 'maturity']):
            return 'datetime'
        
        # Amount/money fields
        if any(term in field_lower for term in ['amount', 'balance', 'price', 'cost', 'fee', 'interest', 'payment']):
            return 'numeric'
        
        # Status/enum fields
        if any(term in field_lower for term in ['status', 'type', 'state', 'category', 'role']):
            return 'enum'
        
        # Text fields
        if any(term in field_lower for term in ['name', 'description', 'narrative', 'notes', 'address', 'email', 'phone']):
            return 'text'
        
        # Default
        return 'text'
    
    def process_data_file(self, file_path: str, folder: str) -> Dict[str, Any]:
        """Process and analyze data files (CSV/Excel)"""
        file = os.path.basename(file_path)
        file_lower = file.lower()
        table_name = os.path.splitext(file)[0]
        
        try:
            if file_lower.endswith('.csv'):
                # Read only header row from CSV
                with open(file_path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    headers = next(reader, None)
            else:
                # Read Excel file (first sheet only)
                xl = pd.ExcelFile(file_path)
                if len(xl.sheet_names) > 0:
                    df = pd.read_excel(file_path, nrows=1)
                    headers = df.columns.tolist()
                else:
                    headers = []
            
            if headers:
                # Analyze headers for data types and relationships
                analyzed_headers = []
                for header in headers:
                    analyzed_headers.append({
                        'field_name': header,
                        'data_type': self._infer_data_type(header, ''),
                        'is_identifier': any(term in header.lower() for term in ['id', 'key', 'reference']),
                        'is_foreign_key': any(term in header.lower() for term in ['customer', 'account', 'client'])
                    })
                
                table_info = {
                    'database': folder,
                    'table_name': table_name,
                    'file_name': file,
                    'headers': analyzed_headers,
                    'header_count': len(headers)
                }
                
                print(f"\nDatabase: {folder}")
                print(f"Table: {table_name}")
                print(f"File: {file}")
                print(f"Headers: {', '.join(headers)}")
                print("-" * 50)
                
                return table_info
            else:
                return {'error': f'No headers found in {file}'}
                
        except Exception as e:
            print(f"\nError processing {file_path}: {str(e)}")
            return {'error': str(e)}
    
    def analyze_bank_data(self, bank_folder: str) -> Dict[str, Any]:
        """Analyze all data in a bank folder"""
        print(f"\n{'='*80}")
        print(f"PROCESSING: {bank_folder}")
        print('='*80)
        
        bank_path = os.path.join(self.base_path, bank_folder)
        if not os.path.exists(bank_path):
            return {'error': f'Bank folder {bank_folder} not found'}
        
        bank_analysis = {
            'bank_name': bank_folder,
            'schema': None,
            'tables': [],
            'relationships': [],
            'summary': {}
        }
        
        # Process schema file
        schema_file = os.path.join(bank_path, f"{bank_folder}_Schema.xlsx")
        if os.path.exists(schema_file):
            schema_info = self.read_schema_file(schema_file, bank_folder)
            bank_analysis['schema'] = schema_info
        
        # Process data files
        print(f"\n{'*'*40}")
        print(f"FILES IN {bank_folder}:")
        print('*'*40)
        
        for file in sorted(os.listdir(bank_path)):
            file_path = os.path.join(bank_path, file)
            file_lower = file.lower()
            
            # Skip schema files and non-data files
            if file_lower.endswith('_schema.xlsx'):
                continue
            if not (file_lower.endswith('.csv') or file_lower.endswith(('.xlsx', '.xls'))):
                continue
            
            table_info = self.process_data_file(file_path, bank_folder)
            if 'error' not in table_info:
                bank_analysis['tables'].append(table_info)
        
        # Analyze relationships
        bank_analysis['relationships'] = self._analyze_relationships(bank_analysis['tables'])
        
        # Create summary
        bank_analysis['summary'] = {
            'total_tables': len(bank_analysis['tables']),
            'total_fields': sum(len(table['headers']) for table in bank_analysis['tables']),
            'identifier_fields': sum(len([h for h in table['headers'] if h['is_identifier']]) for table in bank_analysis['tables']),
            'foreign_key_fields': sum(len([h for h in table['headers'] if h['is_foreign_key']]) for table in bank_analysis['tables'])
        }
        
        print(f"\n{'='*80}")
        print(f"COMPLETED: {bank_folder}")
        print(f"Summary: {bank_analysis['summary']}")
        print('='*80)
        
        return bank_analysis
    
    def _analyze_relationships(self, tables: List[Dict]) -> List[Dict]:
        """Analyze potential relationships between tables"""
        relationships = []
        
        for table in tables:
            table_name = table['table_name']
            for header in table['headers']:
                if header['is_foreign_key']:
                    # Look for potential parent tables
                    for other_table in tables:
                        if other_table['table_name'] != table_name:
                            for other_header in other_table['headers']:
                                if other_header['is_identifier']:
                                    # Check if this could be a relationship
                                    if self._is_potential_relationship(header['field_name'], other_header['field_name']):
                                        relationships.append({
                                            'child_table': table_name,
                                            'child_field': header['field_name'],
                                            'parent_table': other_table['table_name'],
                                            'parent_field': other_header['field_name'],
                                            'relationship_type': 'foreign_key',
                                            'confidence': 0.8
                                        })
        
        return relationships
    
    def _is_potential_relationship(self, child_field: str, parent_field: str) -> bool:
        """Check if two fields could be related"""
        child_lower = child_field.lower()
        parent_lower = parent_field.lower()
        
        # Direct matches
        if child_lower == parent_lower:
            return True
        
        # Common patterns
        patterns = [
            ('customerid', 'customerid'),
            ('accountid', 'accountid'),
            ('clientkey', 'clientkey'),
            ('encodedkey', 'encodedkey'),
            ('id', 'id')
        ]
        
        for child_pattern, parent_pattern in patterns:
            if child_pattern in child_lower and parent_pattern in parent_lower:
                return True
        
        return False
    
    def generate_gemini_prompt(self, bank1_analysis: Dict, bank2_analysis: Dict) -> str:
        """Generate a comprehensive prompt for Gemini AI analysis"""
        
        prompt = f"""
# BANK DATA INTEGRATION ANALYSIS REQUEST

You are an expert data integration specialist analyzing two banking systems for merger. Please provide detailed analysis and recommendations.

## BANK 1 ANALYSIS ({bank1_analysis['bank_name']})
**Schema Fields ({bank1_analysis['summary']['total_fields']} total):**
"""
        
        if bank1_analysis['schema']:
            for field in bank1_analysis['schema']['fields']:
                prompt += f"- {field['field_name']}: {field['description']} (Type: {field['data_type']})\n"
        
        prompt += f"""
**Tables ({bank1_analysis['summary']['total_tables']} total):**
"""
        
        for table in bank1_analysis['tables']:
            prompt += f"- {table['table_name']}: {table['header_count']} fields\n"
            for header in table['headers']:
                prompt += f"  - {header['field_name']} ({header['data_type']})"
                if header['is_identifier']:
                    prompt += " [IDENTIFIER]"
                if header['is_foreign_key']:
                    prompt += " [FOREIGN_KEY]"
                prompt += "\n"
        
        prompt += f"""
## BANK 2 ANALYSIS ({bank2_analysis['bank_name']})
**Schema Fields ({bank2_analysis['summary']['total_fields']} total):**
"""
        
        if bank2_analysis['schema']:
            for field in bank2_analysis['schema']['fields']:
                prompt += f"- {field['field_name']}: {field['description']} (Type: {field['data_type']})\n"
        
        prompt += f"""
**Tables ({bank2_analysis['summary']['total_tables']} total):**
"""
        
        for table in bank2_analysis['tables']:
            prompt += f"- {table['table_name']}: {table['header_count']} fields\n"
            for header in table['headers']:
                prompt += f"  - {header['field_name']} ({header['data_type']})"
                if header['is_identifier']:
                    prompt += " [IDENTIFIER]"
                if header['is_foreign_key']:
                    prompt += " [FOREIGN_KEY]"
                prompt += "\n"
        
        prompt += """
## ANALYSIS REQUEST

Please provide a comprehensive JSON response with the following structure:

```json
{
  "cross_bank_mappings": [
    {
      "bank1_table": "table_name",
      "bank1_field": "field_name", 
      "bank2_table": "table_name",
      "bank2_field": "field_name",
      "confidence": 0.95,
      "mapping_type": "direct|transformation|semantic",
      "transformation_needed": false,
      "transformation_rule": "if needed"
    }
  ],
  "customer_entity_mapping": {
    "bank1_primary_key": "field_name",
    "bank2_primary_key": "field_name", 
    "merge_strategy": "left_join|inner_join|union",
    "deduplication_rules": ["rule1", "rule2"]
  },
  "account_entity_mapping": {
    "bank1_primary_key": "field_name",
    "bank2_primary_key": "field_name",
    "merge_strategy": "left_join|inner_join|union", 
    "deduplication_rules": ["rule1", "rule2"]
  },
  "transaction_entity_mapping": {
    "bank1_primary_key": "field_name",
    "bank2_primary_key": "field_name",
    "merge_strategy": "left_join|inner_join|union",
    "deduplication_rules": ["rule1", "rule2"]
  },
  "data_quality_issues": [
    {
      "issue_type": "missing_values|format_inconsistency|duplicates",
      "description": "description",
      "affected_tables": ["table1", "table2"],
      "severity": "high|medium|low",
      "recommendation": "how to fix"
    }
  ],
  "merge_recommendations": {
    "unified_schema": {
      "customers": ["field1", "field2", "field3"],
      "accounts": ["field1", "field2", "field3"],
      "transactions": ["field1", "field2", "field3"]
    },
    "data_transformation_rules": [
      {
        "source": "bank1.field",
        "target": "unified.field",
        "transformation": "direct|format|calculate"
      }
    ],
    "final_merge_strategy": "step_by_step_approach"
  }
}
```

Focus on:
1. **Semantic field matching** (e.g., "givenName" vs "firstName")
2. **Data type compatibility** 
3. **Primary key strategies** for entity resolution
4. **Foreign key relationships** preservation
5. **Data quality** assessment and remediation
6. **Unified schema** design for the merged system

Provide specific, actionable recommendations for each mapping with confidence scores.
"""
        
        return prompt
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """Run complete analysis of both banks"""
        print("Starting comprehensive bank data analysis...")
        
        # Analyze both banks
        bank1_analysis = self.analyze_bank_data("Bank 1 Data")
        bank2_analysis = self.analyze_bank_data("Bank 2 Data")
        
        # Generate Gemini prompt
        gemini_prompt = self.generate_gemini_prompt(bank1_analysis, bank2_analysis)
        
        # Save results
        analysis_results = {
            'bank1': bank1_analysis,
            'bank2': bank2_analysis,
            'gemini_prompt': gemini_prompt,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Save to file
        with open('comprehensive_bank_analysis.json', 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f"\n{'='*80}")
        print("ANALYSIS COMPLETE!")
        print(f"Results saved to: comprehensive_bank_analysis.json")
        print(f"Gemini prompt length: {len(gemini_prompt)} characters")
        print('='*80)
        
        return analysis_results

def main():
    analyzer = SchemaAnalyzer()
    results = analyzer.run_full_analysis()
    
    # Print the Gemini prompt for review
    print("\n" + "="*80)
    print("GEMINI AI PROMPT:")
    print("="*80)
    print(results['gemini_prompt'])

if __name__ == "__main__":
    main()
