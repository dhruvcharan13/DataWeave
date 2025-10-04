#!/usr/bin/env python3
"""
Bank Schema Analysis and Mapping Strategy
Analyzes Bank 1 and Bank 2 data structures to identify relationships and mappings
"""

import pandas as pd
import json
from typing import Dict, List, Tuple

class BankSchemaAnalyzer:
    def __init__(self):
        self.bank1_schema = {}
        self.bank2_schema = {}
        self.relationships = []
        self.mappings = []
    
    def analyze_bank_schemas(self):
        """Analyze both bank schemas and identify relationships"""
        
        # Bank 1 Schema Analysis
        print("=== BANK 1 SCHEMA ANALYSIS ===")
        bank1_customer = pd.read_excel('Bank 1 Data/Bank1_Mock_Customer.xlsx')
        bank1_accounts = pd.read_excel('Bank 1 Data/Bank1_Mock_CurSav_Accounts.xlsx')
        bank1_transactions = pd.read_csv('Bank 1 Data/Bank1_Mock_CurSav_Transactions.csv')
        
        self.bank1_schema = {
            'customer': {
                'table': 'Bank1_Customer',
                'primary_key': 'customerId',
                'columns': bank1_customer.columns.tolist(),
                'row_count': len(bank1_customer),
                'key_fields': ['customerId', 'legalId', 'accountOfficerId']
            },
            'accounts': {
                'table': 'Bank1_Accounts',
                'primary_key': 'accountId',
                'foreign_keys': ['customerId', 'productId'],
                'columns': bank1_accounts.columns.tolist(),
                'row_count': len(bank1_accounts),
                'key_fields': ['accountId', 'customerId', 'productId']
            },
            'transactions': {
                'table': 'Bank1_Transactions',
                'primary_key': 'transactionReference',
                'foreign_keys': ['accountId'],
                'columns': bank1_transactions.columns.tolist(),
                'row_count': len(bank1_transactions),
                'key_fields': ['transactionReference', 'accountId']
            }
        }
        
        # Bank 2 Schema Analysis
        print("=== BANK 2 SCHEMA ANALYSIS ===")
        bank2_customer = pd.read_excel('Bank 2 Data/Bank2_Mock_Customer.xlsx')
        bank2_accounts = pd.read_excel('Bank 2 Data/Bank2_Mock_Deposit_Accounts.xlsx')
        
        self.bank2_schema = {
            'customer': {
                'table': 'Bank2_Customer',
                'primary_key': 'encodedKey',
                'columns': bank2_customer.columns.tolist(),
                'row_count': len(bank2_customer),
                'key_fields': ['encodedKey', 'id', 'assignedUserKey']
            },
            'accounts': {
                'table': 'Bank2_Accounts',
                'primary_key': 'encodedKey',
                'foreign_keys': ['accountHolderKey', 'productTypeKey'],
                'columns': bank2_accounts.columns.tolist(),
                'row_count': len(bank2_accounts),
                'key_fields': ['encodedKey', 'id', 'accountHolderKey', 'productTypeKey']
            }
        }
        
        return self.bank1_schema, self.bank2_schema
    
    def identify_relationships(self):
        """Identify relationships within each bank's data"""
        
        # Bank 1 Relationships
        bank1_relationships = [
            {
                'source_table': 'Bank1_Customer',
                'source_column': 'customerId',
                'target_table': 'Bank1_Accounts',
                'target_column': 'customerId',
                'relationship_type': 'one_to_many',
                'description': 'Customer can have multiple accounts'
            },
            {
                'source_table': 'Bank1_Accounts',
                'source_column': 'accountId',
                'target_table': 'Bank1_Transactions',
                'target_column': 'accountId',
                'relationship_type': 'one_to_many',
                'description': 'Account can have multiple transactions'
            }
        ]
        
        # Bank 2 Relationships
        bank2_relationships = [
            {
                'source_table': 'Bank2_Customer',
                'source_column': 'encodedKey',
                'target_table': 'Bank2_Accounts',
                'target_column': 'accountHolderKey',
                'relationship_type': 'one_to_many',
                'description': 'Customer can have multiple accounts'
            }
        ]
        
        self.relationships = bank1_relationships + bank2_relationships
        return self.relationships
    
    def identify_cross_bank_mappings(self):
        """Identify potential mappings between Bank 1 and Bank 2"""
        
        mappings = [
            # Customer Mappings
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'customerId',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'encodedKey',
                'mapping_type': 'primary_key',
                'confidence': 0.9,
                'description': 'Customer primary identifiers'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'givenName',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'firstName',
                'mapping_type': 'field_mapping',
                'confidence': 0.95,
                'description': 'Customer first names'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'lastName',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'lastName',
                'mapping_type': 'field_mapping',
                'confidence': 0.95,
                'description': 'Customer last names'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'email',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'emailAddress',
                'mapping_type': 'field_mapping',
                'confidence': 0.9,
                'description': 'Customer email addresses'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'phoneNumber',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'homePhone',
                'mapping_type': 'field_mapping',
                'confidence': 0.8,
                'description': 'Customer phone numbers'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'dateOfBirth',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'birthDate',
                'mapping_type': 'field_mapping',
                'confidence': 0.95,
                'description': 'Customer birth dates'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'gender',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'gender',
                'mapping_type': 'field_mapping',
                'confidence': 0.95,
                'description': 'Customer gender'
            },
            {
                'bank1_table': 'Bank1_Customer',
                'bank1_column': 'customerType',
                'bank2_table': 'Bank2_Customer',
                'bank2_column': 'clientType',
                'mapping_type': 'field_mapping',
                'confidence': 0.9,
                'description': 'Customer type classification'
            },
            
            # Account Mappings
            {
                'bank1_table': 'Bank1_Accounts',
                'bank1_column': 'accountId',
                'bank2_table': 'Bank2_Accounts',
                'bank2_column': 'encodedKey',
                'mapping_type': 'primary_key',
                'confidence': 0.9,
                'description': 'Account primary identifiers'
            },
            {
                'bank1_table': 'Bank1_Accounts',
                'bank1_column': 'customerId',
                'bank2_table': 'Bank2_Accounts',
                'bank2_column': 'accountHolderKey',
                'mapping_type': 'foreign_key',
                'confidence': 0.9,
                'description': 'Account to customer relationships'
            },
            {
                'bank1_table': 'Bank1_Accounts',
                'bank1_column': 'availableBalance',
                'bank2_table': 'Bank2_Accounts',
                'bank2_column': 'availableBalance',
                'mapping_type': 'field_mapping',
                'confidence': 0.95,
                'description': 'Account available balance'
            },
            {
                'bank1_table': 'Bank1_Accounts',
                'bank1_column': 'currency',
                'bank2_table': 'Bank2_Accounts',
                'bank2_column': 'currencyCode',
                'mapping_type': 'field_mapping',
                'confidence': 0.9,
                'description': 'Account currency'
            }
        ]
        
        self.mappings = mappings
        return self.mappings
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        
        report = {
            'bank1_schema': self.bank1_schema,
            'bank2_schema': self.bank2_schema,
            'relationships': self.relationships,
            'cross_bank_mappings': self.mappings,
            'summary': {
                'bank1_tables': len(self.bank1_schema),
                'bank2_tables': len(self.bank2_schema),
                'internal_relationships': len(self.relationships),
                'cross_bank_mappings': len(self.mappings)
            }
        }
        
        return report
    
    def print_analysis_summary(self):
        """Print analysis summary"""
        print("\n" + "="*60)
        print("BANK SCHEMA ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\nBank 1 Tables: {len(self.bank1_schema)}")
        for table_name, table_info in self.bank1_schema.items():
            print(f"  - {table_info['table']}: {table_info['row_count']} rows, {len(table_info['columns'])} columns")
        
        print(f"\nBank 2 Tables: {len(self.bank2_schema)}")
        for table_name, table_info in self.bank2_schema.items():
            print(f"  - {table_info['table']}: {table_info['row_count']} rows, {len(table_info['columns'])} columns")
        
        print(f"\nInternal Relationships: {len(self.relationships)}")
        for rel in self.relationships:
            print(f"  - {rel['source_table']}.{rel['source_column']} -> {rel['target_table']}.{rel['target_column']}")
        
        print(f"\nCross-Bank Mappings: {len(self.mappings)}")
        for mapping in self.mappings:
            print(f"  - {mapping['bank1_table']}.{mapping['bank1_column']} <-> {mapping['bank2_table']}.{mapping['bank2_column']} (confidence: {mapping['confidence']})")

def main():
    analyzer = BankSchemaAnalyzer()
    
    # Analyze schemas
    bank1_schema, bank2_schema = analyzer.analyze_bank_schemas()
    
    # Identify relationships
    relationships = analyzer.identify_relationships()
    
    # Identify cross-bank mappings
    mappings = analyzer.identify_cross_bank_mappings()
    
    # Generate report
    report = analyzer.generate_analysis_report()
    
    # Print summary
    analyzer.print_analysis_summary()
    
    # Save report
    with open('bank_schema_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Analysis complete! Report saved to bank_schema_analysis.json")

if __name__ == "__main__":
    main()
