#!/usr/bin/env python3
"""
Create enhanced Excel mapping file with proper join keys and validation logic
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_enhanced_validation_mapping():
    """Create enhanced Excel mapping with join keys and proper validation logic."""
    
    print("Creating enhanced data validation mapping with join keys...")
    
    # Enhanced mapping data with join keys
    mappings = [
        {
            'Version': '1.0',
            'Function': 'Customer Data Validation',
            'Source_Table': 'customer_source',
            'Target_Table': 'customer_target', 
            'Join_Key': 'customer_id',
            'Source_Column': 'first_name',
            'Target_Column': 'customer_first_name',
            'Derivation_Logic': 'UPPER(source.first_name)',
            'Expected_Result': 'Uppercase transformation of first name',
            'Validation_Type': 'Transformation',
            'Business_Rule': 'Customer names must be uppercase in target system'
        },
        {
            'Version': '1.0',
            'Function': 'Customer Data Validation',
            'Source_Table': 'customer_source',
            'Target_Table': 'customer_target',
            'Join_Key': 'customer_id', 
            'Source_Column': 'last_name',
            'Target_Column': 'customer_last_name',
            'Derivation_Logic': 'UPPER(source.last_name)',
            'Expected_Result': 'Uppercase transformation of last name',
            'Validation_Type': 'Transformation',
            'Business_Rule': 'Customer names must be uppercase in target system'
        },
        {
            'Version': '1.0',
            'Function': 'Account Balance Validation',
            'Source_Table': 'account_source',
            'Target_Table': 'account_target',
            'Join_Key': 'account_id',
            'Source_Column': 'balance_usd, exchange_rate',
            'Target_Column': 'balance_local_currency',
            'Derivation_Logic': 'source.balance_usd * source.exchange_rate',
            'Expected_Result': 'Currency converted balance',
            'Validation_Type': 'Calculation',
            'Business_Rule': 'Local currency balance = USD balance * exchange rate'
        },
        {
            'Version': '1.0',
            'Function': 'Credit Score Assessment',
            'Source_Table': 'customer_source',
            'Target_Table': 'risk_target',
            'Join_Key': 'customer_id',
            'Source_Column': 'credit_score',
            'Target_Column': 'risk_category',
            'Derivation_Logic': 'CASE WHEN source.credit_score >= 750 THEN "LOW" WHEN source.credit_score >= 650 THEN "MEDIUM" ELSE "HIGH" END',
            'Expected_Result': 'Risk category based on credit score',
            'Validation_Type': 'Business_Logic',
            'Business_Rule': 'Risk categorization: 750+ = LOW, 650+ = MEDIUM, <650 = HIGH'
        },
        {
            'Version': '1.0',
            'Function': 'Transaction Fee Calculation',
            'Source_Table': 'transaction_source',
            'Target_Table': 'transaction_target',
            'Join_Key': 'transaction_id',
            'Source_Column': 'amount, fee_rate',
            'Target_Column': 'calculated_fee',
            'Derivation_Logic': 'source.amount * source.fee_rate / 100',
            'Expected_Result': 'Fee amount based on transaction amount and rate',
            'Validation_Type': 'Calculation',
            'Business_Rule': 'Transaction fee = amount * fee_rate / 100'
        },
        {
            'Version': '1.0',
            'Function': 'Loan Interest Calculation',
            'Source_Table': 'loan_source',
            'Target_Table': 'loan_target',
            'Join_Key': 'loan_id',
            'Source_Column': 'principal, base_rate, margin',
            'Target_Column': 'effective_rate',
            'Derivation_Logic': 'source.base_rate + source.margin',
            'Expected_Result': 'Effective interest rate',
            'Validation_Type': 'Calculation',
            'Business_Rule': 'Effective rate = base rate + margin'
        },
        {
            'Version': '1.0',
            'Function': 'Account Status Validation',
            'Source_Table': 'account_source',
            'Target_Table': 'account_target',
            'Join_Key': 'account_id',
            'Source_Column': 'balance, last_transaction_date',
            'Target_Column': 'account_status',
            'Derivation_Logic': 'CASE WHEN source.balance > 0 AND DATEDIFF(CURRENT_DATE, source.last_transaction_date) <= 90 THEN "ACTIVE" ELSE "INACTIVE" END',
            'Expected_Result': 'Account status based on balance and activity',
            'Validation_Type': 'Business_Logic',
            'Business_Rule': 'Active if balance > 0 and transaction within 90 days'
        },
        {
            'Version': '1.0',
            'Function': 'Customer Age Calculation',
            'Source_Table': 'customer_source',
            'Target_Table': 'customer_target',
            'Join_Key': 'customer_id',
            'Source_Column': 'date_of_birth',
            'Target_Column': 'age',
            'Derivation_Logic': 'YEAR(CURRENT_DATE) - YEAR(source.date_of_birth)',
            'Expected_Result': 'Customer age in years',
            'Validation_Type': 'Calculation',
            'Business_Rule': 'Age = current year - birth year'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(mappings)
    
    # Add metadata columns
    df['Created_Date'] = datetime.now().strftime('%Y-%m-%d')
    df['Created_By'] = 'Data Validation Framework'
    df['Priority'] = ['High', 'High', 'Critical', 'Critical', 'Medium', 'Medium', 'High', 'Low']
    df['Test_Data_Size'] = [1000, 1000, 5000, 2000, 10000, 3000, 5000, 1000]
    
    return df

def create_sample_test_data():
    """Create sample test data that demonstrates the join-based validation."""
    
    print("Creating sample test data with proper join keys...")
    
    # Sample customer data
    np.random.seed(42)
    n_customers = 1000
    
    customer_source = pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'first_name': [f'John{i}' for i in range(n_customers)],
        'last_name': [f'Doe{i}' for i in range(n_customers)],
        'credit_score': np.random.randint(300, 850, n_customers),
        'date_of_birth': pd.date_range('1960-01-01', '2000-12-31', periods=n_customers)
    })
    
    # Sample account data
    n_accounts = 1500
    account_source = pd.DataFrame({
        'account_id': range(1, n_accounts + 1),
        'customer_id': np.random.choice(range(1, n_customers + 1), n_accounts),
        'balance_usd': np.random.uniform(100, 50000, n_accounts),
        'exchange_rate': np.random.uniform(0.8, 1.5, n_accounts),
        'balance': np.random.uniform(100, 75000, n_accounts),
        'last_transaction_date': pd.date_range('2024-01-01', '2025-07-25', periods=n_accounts)
    })
    
    # Sample transaction data  
    n_transactions = 5000
    transaction_source = pd.DataFrame({
        'transaction_id': range(1, n_transactions + 1),
        'account_id': np.random.choice(range(1, n_accounts + 1), n_transactions),
        'amount': np.random.uniform(10, 5000, n_transactions),
        'fee_rate': np.random.uniform(0.1, 2.5, n_transactions)
    })
    
    # Sample loan data
    n_loans = 800
    loan_source = pd.DataFrame({
        'loan_id': range(1, n_loans + 1),
        'customer_id': np.random.choice(range(1, n_customers + 1), n_loans),
        'principal': np.random.uniform(5000, 500000, n_loans),
        'base_rate': np.random.uniform(2.0, 8.0, n_loans),
        'margin': np.random.uniform(0.5, 3.0, n_loans)
    })
    
    return {
        'customer_source': customer_source,
        'account_source': account_source, 
        'transaction_source': transaction_source,
        'loan_source': loan_source
    }

def main():
    """Create enhanced validation mapping and sample data."""
    
    # Create enhanced mapping
    mapping_df = create_enhanced_validation_mapping()
    
    # Save to Excel with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'enhanced_validation_mapping_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main mapping sheet
        mapping_df.to_excel(writer, sheet_name='Validation_Mapping', index=False)
        
        # Create sample test data
        sample_data = create_sample_test_data()
        
        # Add sample data sheets
        for table_name, data in sample_data.items():
            data.to_excel(writer, sheet_name=table_name, index=False)
        
        # Add documentation sheet
        doc_data = pd.DataFrame({
            'Column': ['Version', 'Function', 'Source_Table', 'Target_Table', 'Join_Key', 
                      'Source_Column', 'Target_Column', 'Derivation_Logic', 'Expected_Result',
                      'Validation_Type', 'Business_Rule'],
            'Description': [
                'Version of the mapping specification',
                'Business function being validated',
                'Source table name for the validation',
                'Target table name for the validation', 
                'Primary key column(s) for joining source and target tables',
                'Source column(s) used in the derivation logic',
                'Target column to be validated',
                'SQL logic for deriving the expected value',
                'Description of what the derivation should produce',
                'Type of validation: Transformation, Calculation, Business_Logic',
                'Business rule description'
            ],
            'Example': [
                '1.0',
                'Customer Data Validation',
                'customer_source',
                'customer_target',
                'customer_id',
                'first_name',
                'customer_first_name',
                'UPPER(source.first_name)',
                'Uppercase transformation of first name',
                'Transformation',
                'Customer names must be uppercase in target system'
            ]
        })
        doc_data.to_excel(writer, sheet_name='Documentation', index=False)
    
    print(f"✅ Enhanced validation mapping created: {filename}")
    print("\n📋 New Excel Structure:")
    print("- Validation_Mapping: Main mapping with join keys")
    print("- customer_source: Sample customer data")
    print("- account_source: Sample account data") 
    print("- transaction_source: Sample transaction data")
    print("- loan_source: Sample loan data")
    print("- Documentation: Column descriptions")
    
    print(f"\n🔑 Key Enhancements:")
    print("- Join_Key column for proper table joining")
    print("- Source_Table and Target_Table separation")
    print("- Complex derivation logic with multiple source columns")
    print("- Business rules documentation")
    print("- Sample test data with matching join keys")
    
    return filename

if __name__ == "__main__":
    filename = main()
