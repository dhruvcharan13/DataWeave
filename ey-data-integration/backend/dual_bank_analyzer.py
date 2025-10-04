import os
import csv
import pandas as pd
from typing import Dict, List, Any, Tuple
import json
from datetime import datetime

class DualBankAnalyzer:
    """Enhanced analyzer that creates separate JSON files for each bank with user correction capabilities"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "/Users/dhruvcharan/Documents/HTVX"
        self.bank1_analysis = {}
        self.bank2_analysis = {}
    
    def analyze_bank_data(self, bank_folder: str) -> Dict[str, Any]:
        """Analyze all data in a bank folder and return structured analysis"""
        print(f"\n{'='*80}")
        print(f"PROCESSING: {bank_folder}")
        print('='*80)
        
        bank_path = os.path.join(self.base_path, bank_folder)
        if not os.path.exists(bank_path):
            return {'error': f'Bank folder {bank_folder} not found'}
        
        bank_analysis = {
            'bank_name': bank_folder,
            'tables': [],
            'relationships': [],
            'summary': {},
            'user_corrections': {
                'relationships': [],
                'column_types': [],
                'field_mappings': []
            },
            'ai_suggestions': {
                'data_quality_issues': [],
                'schema_improvements': []
            },
            'analysis_metadata': {
                'created_at': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
        
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
            if file_lower.startswith('~$'):  # Skip Excel temp files
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
                        'is_foreign_key': self._is_foreign_key_field(header),
                        'sample_values': [],  # Will be populated when data is uploaded
                        'null_count': 0,      # Will be populated when data is uploaded
                        'unique_count': 0     # Will be populated when data is uploaded
                    })
                
                table_info = {
                    'database': folder,
                    'table_name': table_name,
                    'file_name': file,
                    'headers': analyzed_headers,
                    'header_count': len(headers),
                    'postgresql_table': None,  # Will be set when uploaded to Supabase
                    'supabase_storage_url': None,  # Will be set when uploaded to Supabase
                    'row_count': 0,  # Will be populated when data is uploaded
                    'upload_status': 'pending'
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
    
    def _is_foreign_key_field(self, field_name: str) -> bool:
        """Determine if a field is likely a foreign key"""
        field_lower = field_name.lower()
        
        # Common foreign key patterns
        fk_patterns = [
            'customerid',      # customerId
            'accountid',       # accountId  
            'clientkey',       # clientKey
            'parentkey',       # parentKey
            'accountholderkey', # accountHolderKey
            'assigneduserkey',  # assignedUserKey
            'assignedbranchkey', # assignedBranchKey
            'producttypekey',   # productTypeKey
            'userkey',         # userKey
            'branchkey',       # branchKey
            'externalid',      # externalId
            'documentid',      # documentId
            'migrationeventkey' # migrationEventKey
        ]
        
        # Check for exact matches with common FK patterns
        for pattern in fk_patterns:
            if pattern in field_lower:
                return True
        
        # Check for ID fields that reference other entities
        if field_lower.endswith('id') and any(entity in field_lower for entity in ['customer', 'account', 'client', 'user', 'branch', 'product']):
            return True
            
        return False
    
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
                                            'confidence': 0.8,
                                            'user_approved': False,
                                            'user_rejected': False,
                                            'notes': ''
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
    
    def generate_dual_bank_jsons(self):
        """Generate separate JSON files for Bank1 and Bank2"""
        print("Starting dual bank analysis...")
        
        # Analyze both banks
        self.bank1_analysis = self.analyze_bank_data("Bank 1 Data")
        self.bank2_analysis = self.analyze_bank_data("Bank 2 Data")
        
        # Add internal data quality suggestions
        self._add_data_quality_suggestions()
        
        # Save individual JSON files
        self._save_bank_json("Bank1", self.bank1_analysis)
        self._save_bank_json("Bank2", self.bank2_analysis)
        
        print(f"\n{'='*80}")
        print("DUAL BANK ANALYSIS COMPLETE!")
        print(f"Bank1 JSON: bank1_analysis.json")
        print(f"Bank2 JSON: bank2_analysis.json")
        print('='*80)
        
        return {
            'bank1': self.bank1_analysis,
            'bank2': self.bank2_analysis
        }
    
    def _add_data_quality_suggestions(self):
        """Add internal data quality suggestions to both analyses"""
        # Analyze Bank1 data quality
        self.bank1_analysis['ai_suggestions']['data_quality_issues'] = self._analyze_data_quality(self.bank1_analysis)
        self.bank1_analysis['ai_suggestions']['schema_improvements'] = self._suggest_schema_improvements(self.bank1_analysis)
        
        # Analyze Bank2 data quality
        self.bank2_analysis['ai_suggestions']['data_quality_issues'] = self._analyze_data_quality(self.bank2_analysis)
        self.bank2_analysis['ai_suggestions']['schema_improvements'] = self._suggest_schema_improvements(self.bank2_analysis)
    
    def _analyze_data_quality(self, bank_analysis: Dict) -> List[Dict]:
        """Analyze data quality issues within a bank's dataset"""
        issues = []
        
        for table in bank_analysis['tables']:
            table_name = table['table_name']
            
            # Check for potential data quality issues
            for header in table['headers']:
                field_name = header['field_name']
                
                # Check for inconsistent naming conventions
                if '_' in field_name and any(c.isupper() for c in field_name):
                    issues.append({
                        'table': table_name,
                        'field': field_name,
                        'issue_type': 'naming_inconsistency',
                        'description': f'Field "{field_name}" mixes camelCase and snake_case',
                        'severity': 'low',
                        'recommendation': 'Standardize naming convention'
                    })
                
                # Check for potential data type issues
                if header['data_type'] == 'text' and any(term in field_name.lower() for term in ['id', 'key']):
                    issues.append({
                        'table': table_name,
                        'field': field_name,
                        'issue_type': 'data_type_mismatch',
                        'description': f'Field "{field_name}" appears to be an ID but is typed as text',
                        'severity': 'medium',
                        'recommendation': 'Consider changing to identifier type'
                    })
                
                # Check for missing primary keys
                if not any(h['is_identifier'] for h in table['headers']):
                    issues.append({
                        'table': table_name,
                        'field': 'N/A',
                        'issue_type': 'missing_primary_key',
                        'description': f'Table "{table_name}" has no clear primary key',
                        'severity': 'high',
                        'recommendation': 'Identify and mark primary key field'
                    })
                    break  # Only add this once per table
        
        return issues
    
    def _suggest_schema_improvements(self, bank_analysis: Dict) -> List[Dict]:
        """Suggest schema improvements for a bank's dataset"""
        improvements = []
        
        for table in bank_analysis['tables']:
            table_name = table['table_name']
            
            # Suggest adding indexes for foreign keys
            foreign_key_fields = [h for h in table['headers'] if h['is_foreign_key']]
            if foreign_key_fields:
                improvements.append({
                    'table': table_name,
                    'improvement_type': 'indexing',
                    'description': f'Add indexes for foreign key fields: {[f["field_name"] for f in foreign_key_fields]}',
                    'priority': 'medium'
                })
            
            # Suggest data validation rules
            for header in table['headers']:
                field_name = header['field_name']
                
                if header['data_type'] == 'datetime':
                    improvements.append({
                        'table': table_name,
                        'field': field_name,
                        'improvement_type': 'validation',
                        'description': f'Add date validation for field "{field_name}"',
                        'priority': 'low'
                    })
                
                elif header['data_type'] == 'numeric' and 'amount' in field_name.lower():
                    improvements.append({
                        'table': table_name,
                        'field': field_name,
                        'improvement_type': 'validation',
                        'description': f'Add range validation for monetary field "{field_name}"',
                        'priority': 'medium'
                    })
        
        return improvements
    
    def _save_bank_json(self, bank_name: str, analysis: Dict):
        """Save bank analysis to JSON file"""
        filename = f"{bank_name.lower()}_analysis.json"
        
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"Saved {bank_name} analysis to {filename}")
    
    def load_bank_json(self, bank_name: str) -> Dict:
        """Load bank analysis from JSON file"""
        filename = f"{bank_name.lower()}_analysis.json"
        
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            return {'error': f'File {filename} not found'}
    
    def update_user_corrections(self, bank_name: str, corrections: Dict):
        """Update user corrections in the bank JSON file"""
        analysis = self.load_bank_json(bank_name)
        
        if 'error' not in analysis:
            # Update corrections
            if 'relationships' in corrections:
                analysis['user_corrections']['relationships'].extend(corrections['relationships'])
            
            if 'column_types' in corrections:
                analysis['user_corrections']['column_types'].extend(corrections['column_types'])
            
            if 'field_mappings' in corrections:
                analysis['user_corrections']['field_mappings'].extend(corrections['field_mappings'])
            
            # Update metadata
            analysis['analysis_metadata']['last_modified'] = datetime.now().isoformat()
            
            # Save updated file
            self._save_bank_json(bank_name, analysis)
            
            return {'message': f'{bank_name} corrections updated successfully'}
        else:
            return analysis

def main():
    analyzer = DualBankAnalyzer()
    results = analyzer.generate_dual_bank_jsons()
    
    print("\n" + "="*80)
    print("DUAL BANK ANALYSIS SUMMARY:")
    print("="*80)
    print(f"Bank1: {results['bank1']['summary']['total_tables']} tables, {results['bank1']['summary']['total_fields']} fields")
    print(f"Bank2: {results['bank2']['summary']['total_tables']} tables, {results['bank2']['summary']['total_fields']} fields")
    print(f"Bank1 relationships: {len(results['bank1']['relationships'])}")
    print(f"Bank2 relationships: {len(results['bank2']['relationships'])}")

if __name__ == "__main__":
    main()
