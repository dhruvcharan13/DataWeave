import pandas as pd
import numpy as np
import json
import os
import uuid
from datetime import datetime
import re

class BankDataMerger:
    def __init__(self, mapping_file_path, bank1_dir, bank2_dir, output_dir):
        self.mapping_file_path = mapping_file_path
        self.bank1_dir = bank1_dir
        self.bank2_dir = bank2_dir
        self.output_dir = output_dir
        self.mapping_data = None
        self.loaded_data = {}
        self.merged_data = {}
        
        # Default file mappings as fallback
        self.default_bank1_files = {
            "Customer": "Bank1_Mock_Customer.xlsx",
            "CurSav Accounts": "Bank1_Mock_CurSav_Accounts.xlsx", 
            "Fixed Term Accounts": "Bank1_Mock_FixedTerm_Accounts.xlsx",
            "Loan Accounts": "Bank1_Mock_Loan_Accounts.xlsx",
            "CurSav Account Transactions": "Bank1_Mock_CurSav_Transactions.csv",
            "Fixed Term Account Transactions": "Bank1_Mock_FixedTerm_Transactions.csv",
            "Loan Account Transactions": "Bank1_Mock_Loan_Transactions.csv"
        }
        
        self.default_bank2_files = {
            "Customer": "Bank2_Mock_Customer.xlsx",
            "Addresses": "Bank2_Mock_Addresses.xlsx",
            "Identifications": "Bank2_Mock_Identifications.xlsx",
            "Deposit Accounts": "Bank2_Mock_Deposit_Accounts.xlsx",
            "Loan Accounts": "Bank2_Mock_Loan_Accounts.xlsx",
            "Deposit Account Transactions": "Bank2_Mock_Deposit_Transactions.xlsx",
            "Loan Account Transactions": "Bank2_Mock_Loan_Transactions.xlsx"
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
    def load_mapping_data(self):
        """Load the mapping JSON file and extract file mappings"""
        with open(self.mapping_file_path, 'r', encoding='utf-8') as f:
            self.mapping_data = json.load(f)
        print("✓ Mapping data loaded successfully")
        
        # Extract file mappings from the JSON structure with fallbacks
        try:
            self.bank1_files = self.mapping_data['source_dataset'].get('files', self.default_bank1_files)
            print(f"✓ Using Bank1 file mappings from JSON")
        except (KeyError, AttributeError):
            self.bank1_files = self.default_bank1_files
            print(f"✓ Using default Bank1 file mappings")
            
        try:
            self.bank2_files = self.mapping_data['target_dataset'].get('files', self.default_bank2_files)
            print(f"✓ Using Bank2 file mappings from JSON")
        except (KeyError, AttributeError):
            self.bank2_files = self.default_bank2_files
            print(f"✓ Using default Bank2 file mappings")
        
        print(f"  Bank1 files: {len(self.bank1_files)} tables")
        print(f"  Bank2 files: {len(self.bank2_files)} tables")
        
    def load_bank_files(self):
        """Load all Bank1 and Bank2 files based on available mappings"""
        print("Loading Bank1 files...")
        for table_name, filename in self.bank1_files.items():
            file_path = os.path.join(self.bank1_dir, filename)
            if os.path.exists(file_path):
                try:
                    if filename.endswith('.xlsx'):
                        self.loaded_data[f"bank1_{table_name}"] = pd.read_excel(file_path)
                    elif filename.endswith('.csv'):
                        self.loaded_data[f"bank1_{table_name}"] = pd.read_csv(file_path)
                    print(f"  ✓ Loaded {table_name} from {filename}")
                    # Print column info for debugging
                    df = self.loaded_data[f"bank1_{table_name}"]
                    print(f"    Columns: {list(df.columns)}")
                    if len(df) > 0:
                        print(f"    Sample data shape: {df.shape}")
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  ✗ File not found: {file_path}")
                
        print("Loading Bank2 files...")
        for table_name, filename in self.bank2_files.items():
            file_path = os.path.join(self.bank2_dir, filename)
            if os.path.exists(file_path):
                try:
                    if filename.endswith('.xlsx'):
                        self.loaded_data[f"bank2_{table_name}"] = pd.read_excel(file_path)
                    elif filename.endswith('.csv'):
                        self.loaded_data[f"bank2_{table_name}"] = pd.read_csv(file_path)
                    print(f"  ✓ Loaded {table_name} from {filename}")
                    # Print column info for debugging
                    df = self.loaded_data[f"bank2_{table_name}"]
                    print(f"    Columns: {list(df.columns)}")
                    if len(df) > 0:
                        print(f"    Sample data shape: {df.shape}")
                except Exception as e:
                    print(f"  ✗ Error loading {filename}: {str(e)}")
            else:
                print(f"  ✗ File not found: {file_path}")
                
    def generate_uuid(self, seed_string):
        """Generate deterministic UUID based on seed string"""
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(seed_string)))
    
    def normalize_phone(self, phone):
        """Standardize phone number to E.164 format"""
        if pd.isna(phone):
            return phone
            
        phone_str = str(phone)
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone_str)
        
        if len(digits) == 10:
            return f"+1{digits}"  # Assume US/Canada
        elif len(digits) == 11 and digits.startswith('1'):
            return f"+{digits}"
        elif len(digits) > 11:
            return f"+{digits}"
        else:
            return phone_str  # Return original if can't standardize
    
    def parse_date(self, date_str, output_format='%Y-%m-%d'):
        """Parse date string to standardized format"""
        if pd.isna(date_str):
            return date_str
            
        if isinstance(date_str, datetime):
            return date_str.strftime(output_format)
            
        if hasattr(date_str, 'strftime'):
            return date_str.strftime(output_format)
            
        date_str = str(date_str)
        
        # Try common date formats
        formats = [
            '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%m-%d-%Y', '%d-%m-%Y', '%Y.%m.%d', '%d.%m.%Y',
            '%Y%m%d', '%d%m%Y', '%m%d%Y'
        ]
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime(output_format)
            except ValueError:
                continue
                
        # Return original if can't parse
        return date_str
    
    def normalize_country_code(self, country):
        """Convert country name to ISO 3166-1 alpha-3 code"""
        if pd.isna(country):
            return country
            
        country = str(country).upper().strip()
        
        # Simple country code mapping (in practice, use a comprehensive library)
        country_mapping = {
            'UNITED STATES': 'USA', 'US': 'USA', 'USA': 'USA', 'UNITED STATES OF AMERICA': 'USA',
            'UNITED KINGDOM': 'GBR', 'UK': 'GBR', 'GREAT BRITAIN': 'GBR',
            'CANADA': 'CAN', 'CA': 'CAN',
            'GERMANY': 'DEU', 'DE': 'DEU',
            'FRANCE': 'FRA', 'FR': 'FRA',
            'AUSTRALIA': 'AUS', 'AU': 'AUS',
            'JAPAN': 'JPN', 'JP': 'JPN',
            'CHINA': 'CHN', 'CN': 'CHN',
            'INDIA': 'IND', 'IN': 'IND'
        }
        
        return country_mapping.get(country, country[:3].upper() if len(country) >= 3 else country)
    
    def normalize_currency_code(self, currency):
        """Convert currency to ISO 4217 code"""
        if pd.isna(currency):
            return currency
            
        currency = str(currency).upper().strip()
        
        currency_mapping = {
            'USD': 'USD', 'US$': 'USD', '$': 'USD', 'US DOLLAR': 'USD',
            'EUR': 'EUR', 'EURO': 'EUR', '€': 'EUR',
            'GBP': 'GBP', 'POUND': 'GBP', '£': 'GBP', 'BRITISH POUND': 'GBP',
            'JPY': 'JPY', 'YEN': 'JPY', '¥': 'JPY',
            'CAD': 'CAD', 'CA$': 'CAD', 'CANADIAN DOLLAR': 'CAD',
            'AUD': 'AUD', 'AUSTRALIAN DOLLAR': 'AUD',
            'INR': 'INR', 'RUPEE': 'INR', '₹': 'INR'
        }
        
        return currency_mapping.get(currency, currency)
    
    def normalize_string(self, text, case_type='proper'):
        """Normalize string case and trim"""
        if pd.isna(text):
            return text
            
        text = str(text).strip()
        
        if case_type == 'upper':
            return text.upper()
        elif case_type == 'lower':
            return text.lower()
        elif case_type == 'proper':
            return text.title()
        else:
            return text
    
    def cast_to_decimal(self, value, precision=15, scale=2):
        """Cast value to decimal with specified precision"""
        if pd.isna(value):
            return value
            
        try:
            # Round to specified decimal places
            return round(float(value), scale)
        except (ValueError, TypeError):
            return value
    
    def apply_transformation(self, value, transform_type, params):
        """Apply transformation to a value based on transform type and parameters"""
        if pd.isna(value):
            return value
            
        try:
            if transform_type == 'identity':
                return value
                
            elif transform_type == 'cast':
                if params.get('type') == 'decimal':
                    return self.cast_to_decimal(value, params.get('precision', 15), params.get('scale', 2))
                elif params.get('type') == 'integer':
                    return int(float(value)) if value else value
                    
            elif transform_type == 'parse_date':
                return self.parse_date(value)
                
            elif transform_type == 'string_normalize':
                case = params.get('case', 'proper')
                mapping = params.get('mapping', {})
                
                # Apply case normalization
                result = self.normalize_string(value, case)
                
                # Apply value mapping if specified
                if mapping and isinstance(mapping, dict):
                    if result.upper() in mapping:
                        return mapping[result.upper()]
                    # Also check original value
                    if str(value).upper() in mapping:
                        return mapping[str(value).upper()]
                elif mapping == 'iso_3166_alpha3':
                    return self.normalize_country_code(result)
                elif mapping == 'iso_4217':
                    return self.normalize_currency_code(result)
                    
                return result
                
            elif transform_type == 'custom':
                rule = params.get('rule', '')
                if 'phone' in rule.lower() or 'E.164' in rule:
                    return self.normalize_phone(value)
                elif 'UUID' in rule:
                    return self.generate_uuid(value)
                    
            return value
            
        except Exception as e:
            print(f"Warning: Transformation failed for value {value}: {e}")
            return value

    def get_mappings_for_table(self, target_table):
        """Get all mappings for a specific target table"""
        if 'mappings' not in self.mapping_data:
            return []
        return [m for m in self.mapping_data['mappings'] 
                if m['target']['table'] == target_table]

    def get_output_plans(self):
        """Get output plans from JSON or generate default ones"""
        if 'output_plans' in self.mapping_data:
            return self.mapping_data['output_plans']
        else:
            # Generate default output plans based on available tables
            return self.generate_default_output_plans()

    def generate_default_output_plans(self):
        """Generate default output plans based on available Bank2 tables"""
        plans = []
        
        # Customer table
        if 'Customer' in self.bank2_files:
            plans.append({
                "output_table": "Customer",
                "join": {
                    "type": "full_outer",
                    "left": {"table": "Customer", "on": ["customerId"]},
                    "right": {"table": "Customer", "on": ["id"]}
                },
                "dedupe": {
                    "keys": ["id"],
                    "strategy": "prefer_non_null",
                    "tie_breaker": "creationDate"
                },
                "use_mappings": [m['id'] for m in self.mapping_data.get('mappings', []) 
                               if m['target']['table'] == 'Customer']
            })
        
        # Deposit Accounts (from CurSav + Fixed Term)
        if 'Deposit Accounts' in self.bank2_files:
            plans.append({
                "output_table": "Deposit Accounts", 
                "join": {
                    "type": "full_outer",
                    "left": {"table": "CurSav Accounts", "on": ["accountId"]},
                    "right": {"table": "Deposit Accounts", "on": ["id"]}
                },
                "dedupe": {
                    "keys": ["id"],
                    "strategy": "prefer_non_null", 
                    "tie_breaker": "creationDate"
                },
                "use_mappings": [m['id'] for m in self.mapping_data.get('mappings', [])
                               if m['target']['table'] == 'Deposit Accounts']
            })
        
        # Loan Accounts
        if 'Loan Accounts' in self.bank2_files:
            plans.append({
                "output_table": "Loan Accounts",
                "join": {
                    "type": "full_outer", 
                    "left": {"table": "Loan Accounts", "on": ["accountId"]},
                    "right": {"table": "Loan Accounts", "on": ["id"]}
                },
                "dedupe": {
                    "keys": ["id"],
                    "strategy": "prefer_non_null",
                    "tie_breaker": "creationDate"
                },
                "use_mappings": [m['id'] for m in self.mapping_data.get('mappings', [])
                               if m['target']['table'] == 'Loan Accounts']
            })
            
        return plans

    def process_table_with_plan(self, table_name, plan):
        """Process a table using the output plan from JSON"""
        print(f"Processing {table_name}...")
        
        # Get source tables from the join configuration
        join_config = plan['join']
        left_table = join_config['left']['table']
        right_table = join_config['right']['table']
        
        # Load source data
        left_data = self.loaded_data.get(f"bank1_{left_table}", pd.DataFrame())
        right_data = self.loaded_data.get(f"bank2_{right_table}", pd.DataFrame())
        
        # Get mappings for this table
        mapping_ids = plan.get('use_mappings', [])
        table_mappings = [m for m in self.mapping_data.get('mappings', []) 
                         if m['id'] in mapping_ids]
        
        # Transform left (Bank1) data
        left_transformed = pd.DataFrame()
        for mapping in table_mappings:
            source_col = mapping['source']['column']
            target_col = mapping['target']['column']
            
            if source_col in left_data.columns:
                transformed_values = left_data[source_col].apply(
                    lambda x: self.apply_transformation(x, mapping['transform']['type'], mapping['transform']['params'])
                )
                left_transformed[target_col] = transformed_values
                
                # Handle UUID generation for encodedKey
                if target_col == 'encodedKey' and mapping['transform']['type'] == 'custom':
                    if 'customerId' in left_data.columns:
                        left_transformed[target_col] = left_data['customerId'].apply(self.generate_uuid)
                    elif 'accountId' in left_data.columns:
                        left_transformed[target_col] = left_data['accountId'].apply(
                            lambda x: self.generate_uuid(f"{table_name.lower()}_{x}")
                        )
        
        # Ensure all target columns are present
        if not right_data.empty:
            for col in right_data.columns:
                if col not in left_transformed.columns:
                    left_transformed[col] = None
        
        # Perform the join
        join_type = join_config['type']
        left_on = join_config['left']['on']
        right_on = join_config['right']['on']
        
        if not left_transformed.empty and not right_data.empty and left_on and right_on:
            if join_type == 'full_outer':
                merged_data = pd.merge(
                    left_transformed, 
                    right_data, 
                    left_on=left_on[0],
                    right_on=right_on[0],
                    how='outer', 
                    suffixes=('_bank1', '_bank2')
                )
                
                # Resolve conflicts according to dedupe strategy
                dedupe_config = plan['dedupe']
                for col in right_data.columns:
                    bank1_col = f"{col}_bank1"
                    bank2_col = f"{col}_bank2"
                    if bank1_col in merged_data.columns and bank2_col in merged_data.columns:
                        if dedupe_config['strategy'] == 'prefer_non_null':
                            merged_data[col] = merged_data[bank2_col].combine_first(merged_data[bank1_col])
                        elif dedupe_config['strategy'] == 'prefer_right_non_null':
                            merged_data[col] = merged_data[bank2_col].combine_first(merged_data[bank1_col])
                
                # Keep only resolved columns
                final_columns = [col for col in right_data.columns if col in merged_data.columns]
                merged_data = merged_data[final_columns]
            else:
                # For other join types, use left transformed as base
                merged_data = left_transformed
        elif not left_transformed.empty:
            merged_data = left_transformed
        else:
            merged_data = right_data
        
        self.merged_data[table_name] = merged_data
        print(f"✓ {table_name} processed: {len(merged_data)} records")

    def process_normalized_tables(self):
        """Process normalized tables (Addresses, Identifications)"""
        print("Processing normalized tables...")
        
        # Process Addresses if mappings exist
        address_mappings = self.get_mappings_for_table('Addresses')
        if address_mappings and 'Customer' in self.bank1_files:
            self.process_normalized_table('Addresses', 'Customer', 'parentKey')
        
        # Process Identifications if mappings exist  
        id_mappings = self.get_mappings_for_table('Identifications')
        if id_mappings and 'Customer' in self.bank1_files:
            self.process_normalized_table('Identifications', 'Customer', 'clientKey')

    def process_normalized_table(self, target_table, source_table, foreign_key):
        """Process a normalized table that extracts data from a source table"""
        print(f"Processing {target_table}...")
        
        bank1_source = self.loaded_data.get(f"bank1_{source_table}", pd.DataFrame())
        bank2_target = self.loaded_data.get(f"bank2_{target_table}", pd.DataFrame())
        
        if bank1_source.empty:
            self.merged_data[target_table] = bank2_target
            return
        
        # Create normalized data from Bank1 source
        bank1_normalized = pd.DataFrame()
        
        # Get mappings for this table
        table_mappings = self.get_mappings_for_table(target_table)
        
        for mapping in table_mappings:
            source_col = mapping['source']['column']
            target_col = mapping['target']['column']
            
            if source_col in bank1_source.columns:
                transformed_values = bank1_source[source_col].apply(
                    lambda x: self.apply_transformation(x, mapping['transform']['type'], mapping['transform']['params'])
                )
                bank1_normalized[target_col] = transformed_values
        
        # Add keys
        if 'customerId' in bank1_source.columns:
            bank1_normalized['encodedKey'] = bank1_source['customerId'].apply(
                lambda x: self.generate_uuid(f"{target_table.lower()}_{x}")
            )
            bank1_normalized[foreign_key] = bank1_source['customerId'].apply(self.generate_uuid)
        
        # Ensure all Bank2 columns are present
        if not bank2_target.empty:
            for col in bank2_target.columns:
                if col not in bank1_normalized.columns:
                    bank1_normalized[col] = None
        
        # Combine with existing Bank2 data
        merged_data = pd.concat([bank2_target, bank1_normalized], ignore_index=True)
        self.merged_data[target_table] = merged_data
        print(f"✓ {target_table} created: {len(merged_data)} records")

    def process_transaction_tables(self):
        """Process transaction tables"""
        print("Processing transaction tables...")
        
        # Deposit transactions (from CurSav + Fixed Term)
        deposit_tx_mappings = self.get_mappings_for_table('Deposit Account Transactions')
        if deposit_tx_mappings:
            self.process_deposit_transactions()
        
        # Loan transactions
        loan_tx_mappings = self.get_mappings_for_table('Loan Account Transactions') 
        if loan_tx_mappings:
            self.process_loan_transactions()

    def process_deposit_transactions(self):
        """Process deposit transactions from CurSav and Fixed Term"""
        bank1_cursav_tx = self.loaded_data.get('bank1_CurSav Account Transactions', pd.DataFrame())
        bank1_fixedterm_tx = self.loaded_data.get('bank1_Fixed Term Account Transactions', pd.DataFrame())
        bank2_deposit_tx = self.loaded_data.get('bank2_Deposit Account Transactions', pd.DataFrame())
        
        # Transform Bank1 transactions
        bank1_transformed_tx = pd.DataFrame()
        
        deposit_tx_mappings = self.get_mappings_for_table('Deposit Account Transactions')
        
        # Process CurSav transactions
        if not bank1_cursav_tx.empty:
            cursav_data = pd.DataFrame()
            for mapping in deposit_tx_mappings:
                source_col = mapping['source']['column']
                target_col = mapping['target']['column']
                
                if source_col in bank1_cursav_tx.columns:
                    transformed_values = bank1_cursav_tx[source_col].apply(
                        lambda x: self.apply_transformation(x, mapping['transform']['type'], mapping['transform']['params'])
                    )
                    cursav_data[target_col] = transformed_values
            
            # Add keys
            if 'transactionReference' in bank1_cursav_tx.columns:
                cursav_data['encodedKey'] = bank1_cursav_tx['transactionReference'].apply(
                    lambda x: self.generate_uuid(f"deposit_tx_{x}")
                )
            if 'accountId' in bank1_cursav_tx.columns:
                cursav_data['parentAccountKey'] = bank1_cursav_tx['accountId'].apply(
                    lambda x: self.generate_uuid(f"deposit_{x}")
                )
            
            bank1_transformed_tx = pd.concat([bank1_transformed_tx, cursav_data], ignore_index=True)
        
        # Process Fixed Term transactions
        if not bank1_fixedterm_tx.empty:
            fixedterm_data = pd.DataFrame()
            for mapping in deposit_tx_mappings:
                source_col = mapping['source']['column']
                target_col = mapping['target']['column']
                
                if source_col in bank1_fixedterm_tx.columns:
                    transformed_values = bank1_fixedterm_tx[source_col].apply(
                        lambda x: self.apply_transformation(x, mapping['transform']['type'], mapping['transform']['params'])
                    )
                    fixedterm_data[target_col] = transformed_values
            
            # Add keys
            if 'transactionReference' in bank1_fixedterm_tx.columns:
                fixedterm_data['encodedKey'] = bank1_fixedterm_tx['transactionReference'].apply(
                    lambda x: self.generate_uuid(f"deposit_tx_{x}")
                )
            if 'accountId' in bank1_fixedterm_tx.columns:
                fixedterm_data['parentAccountKey'] = bank1_fixedterm_tx['accountId'].apply(
                    lambda x: self.generate_uuid(f"deposit_{x}")
                )
            
            bank1_transformed_tx = pd.concat([bank1_transformed_tx, fixedterm_data], ignore_index=True)
        
        # Ensure all Bank2 columns are present
        if not bank2_deposit_tx.empty:
            for col in bank2_deposit_tx.columns:
                if col not in bank1_transformed_tx.columns:
                    bank1_transformed_tx[col] = None
        
        # Merge with Bank2 transactions
        if not bank1_transformed_tx.empty:
            merged_tx = pd.concat([bank2_deposit_tx, bank1_transformed_tx], ignore_index=True)
        else:
            merged_tx = bank2_deposit_tx
        
        self.merged_data['Deposit Account Transactions'] = merged_tx
        print(f"✓ Deposit Transactions processed: {len(merged_tx)} records")

    def process_loan_transactions(self):
        """Process loan transactions"""
        bank1_loan_tx = self.loaded_data.get('bank1_Loan Account Transactions', pd.DataFrame())
        bank2_loan_tx = self.loaded_data.get('bank2_Loan Account Transactions', pd.DataFrame())
        
        bank1_transformed_tx = pd.DataFrame()
        
        if not bank1_loan_tx.empty:
            loan_tx_mappings = self.get_mappings_for_table('Loan Account Transactions')
            
            for mapping in loan_tx_mappings:
                source_col = mapping['source']['column']
                target_col = mapping['target']['column']
                
                if source_col in bank1_loan_tx.columns:
                    transformed_values = bank1_loan_tx[source_col].apply(
                        lambda x: self.apply_transformation(x, mapping['transform']['type'], mapping['transform']['params'])
                    )
                    bank1_transformed_tx[target_col] = transformed_values
            
            # Add keys
            if 'transactionReference' in bank1_loan_tx.columns:
                bank1_transformed_tx['encodedKey'] = bank1_loan_tx['transactionReference'].apply(
                    lambda x: self.generate_uuid(f"loan_tx_{x}")
                )
            if 'accountId' in bank1_loan_tx.columns:
                bank1_transformed_tx['parentAccountKey'] = bank1_loan_tx['accountId'].apply(
                    lambda x: self.generate_uuid(f"loan_{x}")
                )
        
        # Ensure all Bank2 columns are present
        if not bank2_loan_tx.empty:
            for col in bank2_loan_tx.columns:
                if col not in bank1_transformed_tx.columns:
                    bank1_transformed_tx[col] = None
        
        # Merge with Bank2 transactions
        if not bank1_transformed_tx.empty:
            merged_tx = pd.concat([bank2_loan_tx, bank1_transformed_tx], ignore_index=True)
        else:
            merged_tx = bank2_loan_tx
        
        self.merged_data['Loan Account Transactions'] = merged_tx
        print(f"✓ Loan Transactions processed: {len(merged_tx)} records")

    def create_extras_tables(self):
        """Create extras tables for stray fields based on JSON mapping"""
        print("Creating extras tables for stray fields...")
        
        if 'mappings' not in self.mapping_data:
            return
            
        # Find all mappings with extra_field_handling
        extras_mappings = [m for m in self.mapping_data['mappings'] 
                          if m.get('extra_field_handling')]
        
        # Group by target table
        extras_by_table = {}
        for mapping in extras_mappings:
            handling = mapping['extra_field_handling']
            target_table = handling['target_table']
            if target_table not in extras_by_table:
                extras_by_table[target_table] = []
            extras_by_table[target_table].append(mapping)
        
        # Create each extras table
        for target_table, mappings in extras_by_table.items():
            print(f"Creating {target_table}...")
            
            # Determine source table from first mapping
            source_table = mappings[0]['source']['table']
            link_key = mappings[0]['extra_field_handling']['link_key']
            
            bank1_source = self.loaded_data.get(f"bank1_{source_table}", pd.DataFrame())
            
            if bank1_source.empty:
                continue
            
            # Create extras table
            extras_data = pd.DataFrame()
            
            # Add link key
            if link_key in bank1_source.columns:
                extras_data[link_key] = bank1_source[link_key]
            
            # Add stray fields
            for mapping in mappings:
                source_col = mapping['source']['column']
                target_col = mapping['target']['column']
                
                if source_col in bank1_source.columns:
                    extras_data[target_col] = bank1_source[source_col]
            
            if len(extras_data.columns) > 1:  # More than just link key
                self.merged_data[target_table] = extras_data
                print(f"✓ {target_table} created: {len(extras_data)} records")

    def save_merged_data(self):
        """Save all merged tables to output directory"""
        print(f"Saving merged data to {self.output_dir}...")
        
        for table_name, data in self.merged_data.items():
            if not data.empty:
                # Clean table name for filename
                clean_name = table_name.replace(' ', '_').replace('/', '_')
                output_path = os.path.join(self.output_dir, f"Merged_{clean_name}.xlsx")
                
                try:
                    # Save to Excel
                    data.to_excel(output_path, index=False)
                    print(f"  ✓ Saved {table_name}: {len(data)} records, {len(data.columns)} columns")
                    
                    # Also save as CSV for good measure
                    csv_path = os.path.join(self.output_dir, f"Merged_{clean_name}.csv")
                    data.to_csv(csv_path, index=False)
                except Exception as e:
                    print(f"  ✗ Error saving {table_name}: {str(e)}")
    
    def generate_documentation(self):
        """Generate documentation markdown file based on JSON mapping"""
        doc_path = os.path.join(self.output_dir, "MERGE_DOCUMENTATION.md")
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write("# Bank Data Merge Documentation\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            source_name = self.mapping_data.get('source_dataset', {}).get('name', 'Bank1')
            target_name = self.mapping_data.get('target_dataset', {}).get('name', 'Bank2')
            
            f.write("## Overview\n\n")
            f.write(f"This dataset represents the merged banking data from {source_name} and {target_name} systems.\n\n")
            
            f.write("## Source Datasets\n\n")
            f.write(f"- **{source_name}**: Core banking system\n")
            f.write(f"- **{target_name}**: Analytics platform\n\n")
            
            f.write("## Merge Strategy\n\n")
            f.write("### Key Approach:\n")
            f.write("- Schema-driven merging based on JSON mapping specification\n")
            f.write("- Data transformations applied according to mapping rules\n")
            f.write("- No data loss policy with extras tables for unmapped fields\n\n")
            
            f.write("### Applied Transformations:\n\n")
            if 'applied_transformations' in self.mapping_data:
                for transform in self.mapping_data['applied_transformations']:
                    f.write(f"- **{transform['table']}.{transform['column']}**: {transform['description']}\n")
            else:
                f.write("- Transformations applied according to mapping specifications\n")
            
            f.write("\n## Output Tables\n\n")
            for table_name, data in self.merged_data.items():
                f.write(f"### {table_name}\n")
                f.write(f"- **Records**: {len(data)}\n")
                f.write(f"- **Columns**: {len(data.columns)}\n")
                if len(data.columns) > 0:
                    f.write(f"- **Columns**: {', '.join(list(data.columns)[:8])}{'...' if len(data.columns) > 8 else ''}\n\n")
            
            f.write("## Data Quality Notes\n\n")
            f.write("- All transformations applied according to mapping specification\n")
            f.write("- UUIDs generated for all encodedKey fields\n")
            f.write("- Data integrity maintained through proper key relationships\n")
            
            # Add mapping statistics
            f.write("\n## Mapping Statistics\n\n")
            total_mappings = len(self.mapping_data.get('mappings', []))
            f.write(f"- **Total Mappings**: {total_mappings}\n")
            f.write(f"- **Output Tables**: {len(self.merged_data)}\n")
            f.write(f"- **Total Records**: {sum(len(data) for data in self.merged_data.values())}\n")
        
        print(f"✓ Documentation generated: {doc_path}")
    
    def run_merge(self):
        """Execute the complete merge process following JSON recipe"""
        print("Starting Bank Data Merge Process...")
        print("=" * 50)
        
        try:
            # Load the recipe
            self.load_mapping_data()
            self.load_bank_files()
            
            # Process tables according to output_plans in JSON
            output_plans = self.get_output_plans()
            for plan in output_plans:
                self.process_table_with_plan(plan['output_table'], plan)
            
            # Process normalized tables
            self.process_normalized_tables()
            
            # Process transaction tables
            self.process_transaction_tables()
            
            # Create extras tables
            self.create_extras_tables()
            
            # Save results
            self.save_merged_data()
            self.generate_documentation()
            
            print("=" * 50)
            print("✓ Merge completed successfully!")
            print(f"Output location: {self.output_dir}")
            
            # Summary
            total_records = sum(len(data) for data in self.merged_data.values())
            print(f"Total records across all tables: {total_records}")
            print(f"Total tables created: {len(self.merged_data)}")
            
        except Exception as e:
            print(f"✗ Merge failed: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

# Usage example
if __name__ == "__main__":
    # Configuration
    MAPPING_FILE = "mapping_output.json"  # Path to your mapping JSON file
    BANK1_DIR = "Bank 1 Data"
    BANK2_DIR = "Bank 2 Data" 
    OUTPUT_DIR = "Merged_Bank_Data"
    
    # Create and run merger
    merger = BankDataMerger(MAPPING_FILE, BANK1_DIR, BANK2_DIR, OUTPUT_DIR)
    merger.run_merge()