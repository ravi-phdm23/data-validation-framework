#!/usr/bin/env python3
"""
Create Excel Sample File for BigQuery Test Scenarios
This script generates a comprehensive Excel template with sample test scenarios.
Enhanced with separate Source_Join_Key and Target_Join_Key columns.
"""

import pandas as pd
from datetime import datetime
import os

def create_bigquery_test_scenarios_excel():
    """Create a comprehensive Excel file with BigQuery test scenarios."""
    
    # Main test scenarios data - focused on transformation logic
    # Enhanced with separate join keys for source and target tables
    test_scenarios = [
        {
            'Scenario_ID': 'TXN_001',
            'Scenario_Name': 'Customer Full Name Transformation',
            'Description': 'Concatenate first name and last name to create full name',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
        },
        {
            'Scenario_ID': 'TXN_002',
            'Scenario_Name': 'Account Balance Copy',
            'Description': 'Direct copy of account balance from source to target',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_id',  # Different column name in target
            'Target_Column': 'account_balance',
            'Derivation_Logic': 'balance',
        },
        {
            'Scenario_ID': 'TXN_003',
            'Scenario_Name': 'Customer Risk Level Calculation',
            'Description': 'Calculate risk level based on account balance',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'risk_level',
            'Derivation_Logic': 'CASE WHEN balance > 50000 THEN "LOW" WHEN balance > 10000 THEN "MEDIUM" ELSE "HIGH" END',
        },
        {
            'Scenario_ID': 'TXN_004',
            'Scenario_Name': 'Total Transaction Amount',
            'Description': 'Sum of all transaction amounts per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_id',  # Different column name in target
            'Target_Column': 'total_transaction_amount',
            'Derivation_Logic': 'SUM(amount)',
        },
        {
            'Scenario_ID': 'TXN_005',
            'Scenario_Name': 'Transaction Count',
            'Description': 'Count of transactions per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_id',
            'Target_Column': 'transaction_count',
            'Derivation_Logic': 'COUNT(*)',
        },
        {
            'Scenario_ID': 'TXN_006',
            'Scenario_Name': 'Average Transaction Amount',
            'Description': 'Average transaction amount per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_id',
            'Target_Column': 'avg_transaction_amount',
            'Derivation_Logic': 'AVG(amount)',
        },
        {
            'Scenario_ID': 'TXN_007',
            'Scenario_Name': 'Account Status Flag',
            'Description': 'Active/Inactive status based on balance',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_id',
            'Target_Column': 'account_status',
            'Derivation_Logic': 'CASE WHEN balance > 0 THEN "ACTIVE" ELSE "INACTIVE" END',
        },
        {
            'Scenario_ID': 'TXN_008',
            'Scenario_Name': 'Email Domain Extract',
            'Description': 'Extract domain from customer email address',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'email_domain',
            'Derivation_Logic': 'SUBSTR(email, STRPOS(email, "@") + 1)',
        },
        {
            'Scenario_ID': 'TXN_009',
            'Scenario_Name': 'Customer Age Category',
            'Description': 'Categorize customers by age groups',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'age_category',
            'Derivation_Logic': 'CASE WHEN age < 25 THEN "YOUNG" WHEN age < 50 THEN "MIDDLE" ELSE "SENIOR" END',
        },
        {
            'Scenario_ID': 'TXN_010',
            'Scenario_Name': 'Latest Transaction Date',
            'Description': 'Most recent transaction date per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_id',
            'Target_Column': 'latest_transaction_date',
            'Derivation_Logic': 'MAX(transaction_date)',
        },
        {
            'Scenario_ID': 'TXN_011',
            'Scenario_Name': 'Cross-Table Join Example',
            'Description': 'Example with different join keys in source and target',
            'Source_Table': 'transactions',
            'Target_Table': 'monthly_summaries',
            'Source_Join_Key': 'transaction_id',
            'Target_Join_Key': 'txn_reference_id',  # Completely different column name
            'Target_Column': 'processed_amount',
            'Derivation_Logic': 'amount * 1.05',  # With processing fee
        },
        {
            'Scenario_ID': 'COMP_001',
            'Scenario_Name': 'Composite Key Customer Balance',
            'Description': 'Validate balance using composite key (customer_id + account_type)',
            'Source_Table': 'customers',
            'Target_Table': 'account_type_summary',
            'Source_Join_Key': 'customer_id,account_type',  # Composite key
            'Target_Join_Key': 'cust_id,acct_type',        # Different composite key names
            'Target_Column': 'total_balance',
            'Derivation_Logic': 'balance',
        },
        {
            'Scenario_ID': 'COMP_002',
            'Scenario_Name': 'Monthly Transaction Aggregation',
            'Description': 'Aggregate transactions by account and month using composite keys',
            'Source_Table': 'transactions',
            'Target_Table': 'monthly_account_summary',
            'Source_Join_Key': 'account_number,transaction_date',  # Date will be converted to month
            'Target_Join_Key': 'account_ref,summary_month',        # Different names
            'Target_Column': 'monthly_total',
            'Derivation_Logic': 'SUM(amount)',
        },
        {
            'Scenario_ID': 'COMP_003',
            'Scenario_Name': 'Multi-Dimensional Customer Analysis',
            'Description': 'Customer analysis using city, state, and account type composite key',
            'Source_Table': 'customers',
            'Target_Table': 'regional_analysis',
            'Source_Join_Key': 'city,state,account_type',     # Triple composite key
            'Target_Join_Key': 'location_city,region,acct_category', # Different names
            'Target_Column': 'customer_count',
            'Derivation_Logic': 'COUNT(*)',
        }
    ]
    
    # Create DataFrame
    df_scenarios = pd.DataFrame(test_scenarios)
    
    # Additional sheets for documentation and configuration
    
    # Configuration sheet
    config = pd.DataFrame([
        {'Setting': 'Project_ID', 'Value': 'cohesive-apogee-411113', 'Description': 'Google Cloud Project ID'},
        {'Setting': 'Dataset', 'Value': 'banking_sample_data', 'Description': 'BigQuery dataset name'},
        {'Setting': 'Customer_Table', 'Value': 'customers', 'Description': 'Customer master table'},
        {'Setting': 'Transaction_Table', 'Value': 'transactions', 'Description': 'Transaction fact table'},
        {'Setting': 'Target_Table', 'Value': 'customer_summary', 'Description': 'Default target table for transformations'},
        {'Setting': 'Max_Results_Limit', 'Value': '1000', 'Description': 'Default LIMIT for SELECT queries'},
        {'Setting': 'Timeout_Seconds', 'Value': '300', 'Description': 'Query timeout in seconds'}
    ])
    
    # Column mapping guide
    column_guide = pd.DataFrame([
        {'Column': 'Scenario_ID', 'Description': 'Unique identifier for the validation scenario', 'Required': 'Yes', 'Example': 'TXN_001'},
        {'Column': 'Scenario_Name', 'Description': 'Descriptive name for the scenario', 'Required': 'Yes', 'Example': 'Customer Full Name Transformation'},
        {'Column': 'Description', 'Description': 'Detailed description of what the scenario validates', 'Required': 'No', 'Example': 'Concatenate first name and last name'},
        {'Column': 'Source_Table', 'Description': 'Source table name in BigQuery', 'Required': 'Yes', 'Example': 'customers'},
        {'Column': 'Target_Table', 'Description': 'Target table name for validation', 'Required': 'Yes', 'Example': 'customer_summary'},
        {'Column': 'Source_Join_Key', 'Description': 'Join key column name in SOURCE table (comma-separated for composite keys)', 'Required': 'Yes', 'Example': 'customer_id,account_type'},
        {'Column': 'Target_Join_Key', 'Description': 'Join key column name in TARGET table (comma-separated for composite keys)', 'Required': 'Yes', 'Example': 'cust_id,acct_type'},
        {'Column': 'Target_Column', 'Description': 'Column in target table to validate', 'Required': 'Yes', 'Example': 'full_name'},
        {'Column': 'Derivation_Logic', 'Description': 'SQL expression for transformation logic', 'Required': 'Yes', 'Example': 'CONCAT(first_name, " ", last_name)'}
    ])
    
    # Create Excel file with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'BigQuery_Test_Scenarios_Enhanced_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main scenarios sheet
        df_scenarios.to_excel(writer, sheet_name='Transformation_Logic', index=False)
        
        # Documentation sheets
        config.to_excel(writer, sheet_name='Configuration', index=False)
        column_guide.to_excel(writer, sheet_name='Column_Guide', index=False)
        
        # Instructions sheet
        instructions = pd.DataFrame([
            {'Step': 1, 'Action': 'Review Transformation Logic', 'Description': 'Examine the pre-built transformation scenarios in the Transformation_Logic sheet'},
            {'Step': 2, 'Action': 'Understand Join Keys', 'Description': 'Note that Source_Join_Key and Target_Join_Key can have different column names'},
            {'Step': 3, 'Action': 'Review Derivation Logic', 'Description': 'Review the SQL derivation logic for each target column transformation'},
            {'Step': 4, 'Action': 'Modify Logic', 'Description': 'Update Derivation_Logic column with your specific transformation requirements'},
            {'Step': 5, 'Action': 'Set Join Keys Correctly', 'Description': 'Ensure Source_Join_Key matches the actual column name in source table'},
            {'Step': 6, 'Action': 'Set Target Join Keys', 'Description': 'Ensure Target_Join_Key matches the actual column name in target table'},
            {'Step': 7, 'Action': 'Configure Settings', 'Description': 'Update Configuration sheet with your BigQuery project details'},
            {'Step': 8, 'Action': 'Upload to Streamlit', 'Description': 'Use the Excel Scenarios tab to upload this file for validation'},
            {'Step': 9, 'Action': 'Execute Validation', 'Description': 'Run validation to compare source transformations with target table data'},
            {'Step': 10, 'Action': 'Review Results', 'Description': 'Analyze pass/fail results with detailed SQL logic used'},
            {'Step': 11, 'Action': 'Add Custom Scenarios', 'Description': 'Create additional rows for your specific transformation scenarios'}
        ])
        instructions.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Sample custom scenario template
        custom_template = pd.DataFrame([
            {
                'Scenario_ID': 'CUSTOM_001',
                'Scenario_Name': 'Your Custom Transformation',
                'Description': 'Describe what transformation this performs',
                'Source_Table': 'your_source_table',
                'Target_Table': 'your_target_table',
                'Source_Join_Key': 'source_key_column',
                'Target_Join_Key': 'target_key_column',  # Can be different!
                'Target_Column': 'column_to_validate',
                'Derivation_Logic': 'SQL expression for transformation (e.g., UPPER(first_name))',
            }
        ])
        custom_template.to_excel(writer, sheet_name='Custom_Template', index=False)
        
        # Join Key Examples sheet
        join_examples = pd.DataFrame([
            {
                'Scenario': 'Same Column Names',
                'Source_Table': 'customers',
                'Target_Table': 'customer_summary',
                'Source_Join_Key': 'customer_id',
                'Target_Join_Key': 'customer_id',
                'Notes': 'Both tables use the same column name'
            },
            {
                'Scenario': 'Different Column Names',
                'Source_Table': 'customers',
                'Target_Table': 'customer_profiles',
                'Source_Join_Key': 'customer_id',  
                'Target_Join_Key': 'cust_id',
                'Notes': 'Target table uses abbreviated column name'
            },
            {
                'Scenario': 'Legacy vs Modern',
                'Source_Table': 'transactions',
                'Target_Table': 'transaction_history',
                'Source_Join_Key': 'transaction_id',
                'Target_Join_Key': 'txn_reference_id',
                'Notes': 'Modern source table vs legacy target table naming'
            },
            {
                'Scenario': 'Account Linking',
                'Source_Table': 'transactions',
                'Target_Table': 'account_summaries',
                'Source_Join_Key': 'account_number',
                'Target_Join_Key': 'account_id',
                'Notes': 'Different naming conventions for account identifiers'
            }
        ])
        # Composite Key Examples sheet
        composite_examples = pd.DataFrame([
            {
                'Scenario_Type': 'Single Key',
                'Source_Table': 'customers',
                'Target_Table': 'customer_summary',
                'Source_Join_Key': 'customer_id',
                'Target_Join_Key': 'cust_id',
                'Notes': 'Traditional single column primary key'
            },
            {
                'Scenario_Type': 'Composite Key (2 columns)',
                'Source_Table': 'customers',
                'Target_Table': 'account_type_summary',
                'Source_Join_Key': 'customer_id,account_type',
                'Target_Join_Key': 'cust_id,acct_type',
                'Notes': 'Two-column composite key with different target names'
            },
            {
                'Scenario_Type': 'Composite Key (3 columns)',
                'Source_Table': 'customers',
                'Target_Table': 'regional_analysis',
                'Source_Join_Key': 'city,state,account_type',
                'Target_Join_Key': 'location_city,region,acct_category',
                'Notes': 'Three-column composite key for dimensional analysis'
            },
            {
                'Scenario_Type': 'Date-based Composite',
                'Source_Table': 'transactions',
                'Target_Table': 'monthly_account_summary',
                'Source_Join_Key': 'account_number,transaction_date',
                'Target_Join_Key': 'account_ref,summary_month',
                'Notes': 'Date field transformed to month for aggregation'
            },
            {
                'Scenario_Type': 'Mixed Data Types',
                'Source_Table': 'transactions',
                'Target_Table': 'transaction_categories',
                'Source_Join_Key': 'account_number,amount,transaction_type',
                'Target_Join_Key': 'acct_num,txn_amount,txn_category',
                'Notes': 'Composite key with string, numeric, and categorical data'
            }
        ])
        composite_examples.to_excel(writer, sheet_name='Composite_Key_Examples', index=False)
    
    return filename

if __name__ == "__main__":
    filename = create_bigquery_test_scenarios_excel()
    print(f"✅ Enhanced Transformation Logic Excel file created: {filename}")
    print(f"📍 Location: {os.path.abspath(filename)}")
    print("\n🎯 This file contains:")
    print("  • 11 transformation scenarios with SQL derivation logic")
    print("  • Separate Source_Join_Key and Target_Join_Key columns")
    print("  • Source-to-target column mapping definitions")
    print("  • Configuration settings for BigQuery project")
    print("  • Step-by-step instructions for validation")
    print("  • Join key examples and best practices")
    print("  • Custom transformation template")
    print("\n🚀 Key Features:")
    print("  • ✨ Enhanced with separate join keys for source and target tables")
    print("  • Focused on data transformation validation")
    print("  • SQL derivation logic for target column calculations")
    print("  • Pass/fail validation against target table data")
    print("  • Detailed output with SQL logic tracking")
    print("  • Examples of different join key scenarios")
    print("\n📤 Upload this file in the 'Excel Scenarios' tab of your Streamlit app!")
    print("\n💡 Join Key Benefits:")
    print("  • Handle different column names between source and target tables")
    print("  • Support legacy table structures with different naming conventions")
    print("  • Enable cross-system data validation scenarios")
    print("  • Flexible mapping for complex data transformations")
