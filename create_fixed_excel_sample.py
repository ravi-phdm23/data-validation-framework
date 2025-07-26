#!/usr/bin/env python3
"""
Create Fixed Excel Sample for Transformation Validation
Works only with existing tables: customers and transactions
"""

import pandas as pd
from datetime import datetime
import os

def create_fixed_excel_sample():
    """Create Excel sample that works with existing BigQuery tables only."""
    
    # Test scenarios - updated to work with existing tables only
    test_scenarios = [
        {
            'Scenario_ID': 'TXN_001',
            'Scenario_Name': 'Customer Full Name Transformation',
            'Description': 'Validate concatenation of first_name and last_name from customers table',
            'Source_Table': 'customers',
            'Target_Table': 'customers',
            'Join_Key': 'customer_id',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)'
        },
        {
            'Scenario_ID': 'TXN_002',
            'Scenario_Name': 'Account Balance Validation',
            'Description': 'Validate that balance field exists and has valid values',
            'Source_Table': 'customers',
            'Target_Table': 'customers',
            'Join_Key': 'customer_id',
            'Target_Column': 'account_balance',
            'Derivation_Logic': 'balance'
        },
        {
            'Scenario_ID': 'TXN_003',
            'Scenario_Name': 'Customer Risk Level Calculation',
            'Description': 'Calculate customer risk level based on account balance',
            'Source_Table': 'customers',
            'Target_Table': 'customers',
            'Join_Key': 'customer_id',
            'Target_Column': 'risk_level',
            'Derivation_Logic': 'CASE WHEN balance > 50000 THEN "LOW" WHEN balance > 10000 THEN "MEDIUM" ELSE "HIGH" END'
        },
        {
            'Scenario_ID': 'TXN_004',
            'Scenario_Name': 'Total Transaction Amount',
            'Description': 'Calculate total transaction amount per account',
            'Source_Table': 'transactions',
            'Target_Table': 'transactions',
            'Join_Key': 'account_number',
            'Target_Column': 'total_transaction_amount',
            'Derivation_Logic': 'SUM(amount)'
        },
        {
            'Scenario_ID': 'TXN_005',
            'Scenario_Name': 'Transaction Count',
            'Description': 'Count total number of transactions per account',
            'Source_Table': 'transactions',
            'Target_Table': 'transactions',
            'Join_Key': 'account_number',
            'Target_Column': 'transaction_count',
            'Derivation_Logic': 'COUNT(*)'
        },
        {
            'Scenario_ID': 'TXN_006',
            'Scenario_Name': 'Average Transaction Amount',
            'Description': 'Calculate average transaction amount per account',
            'Source_Table': 'transactions',
            'Target_Table': 'transactions',
            'Join_Key': 'account_number',
            'Target_Column': 'avg_transaction_amount',
            'Derivation_Logic': 'AVG(amount)'
        },
        {
            'Scenario_ID': 'TXN_007',
            'Scenario_Name': 'Account Status Flag',
            'Description': 'Determine account status based on balance',
            'Source_Table': 'customers',
            'Target_Table': 'customers',
            'Join_Key': 'customer_id',
            'Target_Column': 'account_status',
            'Derivation_Logic': 'CASE WHEN balance > 0 THEN "ACTIVE" ELSE "INACTIVE" END'
        },
        {
            'Scenario_ID': 'TXN_008',
            'Scenario_Name': 'Email Domain Extract',
            'Description': 'Extract domain part from customer email addresses',
            'Source_Table': 'customers',
            'Target_Table': 'customers',
            'Join_Key': 'customer_id',
            'Target_Column': 'email_domain',
            'Derivation_Logic': 'SUBSTR(email, STRPOS(email, "@") + 1)'
        },
    ]
    
    # Create DataFrame
    df = pd.DataFrame(test_scenarios)
    
    # Add configuration sheet data
    config_data = [
        {'Setting': 'Project_ID', 'Value': 'cohesive-apogee-411113', 'Description': 'Google Cloud Project ID'},
        {'Setting': 'Dataset_ID', 'Value': 'banking_sample_data', 'Description': 'BigQuery Dataset Name'},
        {'Setting': 'Available_Tables', 'Value': 'customers, transactions', 'Description': 'Tables available in dataset'},
        {'Setting': 'Validation_Type', 'Value': 'Transformation_Logic', 'Description': 'Type of validation performed'},
        {'Setting': 'Updated_For', 'Value': 'Existing_Tables_Only', 'Description': 'Works with existing tables only'}
    ]
    config_df = pd.DataFrame(config_data)
    
    # Create instructions
    instructions_data = [
        {'Step': 1, 'Instruction': 'Upload this Excel file to the Streamlit app'},
        {'Step': 2, 'Instruction': 'Select the Test_Scenarios sheet'},
        {'Step': 3, 'Instruction': 'Click Generate BigQuery Scenarios from Mapping'},
        {'Step': 4, 'Instruction': 'Click Execute All Excel Scenarios'},
        {'Step': 5, 'Instruction': 'View results in the Data Visualization tab'},
        {'Step': 6, 'Instruction': 'Download comprehensive validation report'}
    ]
    instructions_df = pd.DataFrame(instructions_data)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'BigQuery_Test_Scenarios_FIXED_{timestamp}.xlsx'
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Test_Scenarios', index=False)
        config_df.to_excel(writer, sheet_name='Configuration', index=False)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
    
    print(f'✅ FIXED Excel file created: {filename}')
    print(f'📍 Location: {os.path.abspath(filename)}')
    print('🎯 This file contains:')
    print('  • 8 transformation scenarios that work with existing tables')
    print('  • Uses only customers and transactions tables')
    print('  • Tests derivation logic against source data')
    print('  • Configuration and instructions sheets')
    print('📤 Upload this file in the Streamlit app Excel Scenarios tab!')
    
    return filename

if __name__ == "__main__":
    create_fixed_excel_sample()
