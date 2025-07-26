#!/usr/bin/env python3
"""
Create Excel Sample File for BigQuery Test Scenarios
This script generates a comprehensive Excel template with sample test scenarios.
"""

import pandas as pd
from datetime import datetime
import os

def create_bigquery_test_scenarios_excel():
    """Create a comprehensive Excel file with BigQuery test scenarios."""
    
    # Main test scenarios data - focused on transformation logic
    test_scenarios = [
        {
            'Scenario_ID': 'TXN_001',
            'Scenario_Name': 'Customer Full Name Transformation',
            'Description': 'Concatenate first name and last name to create full name',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
        },
        {
            'Scenario_ID': 'TXN_002',
            'Scenario_Name': 'Account Balance Copy',
            'Description': 'Direct copy of account balance from source to target',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'account_balance',
            'Derivation_Logic': 'balance',
        },
        {
            'Scenario_ID': 'TXN_003',
            'Scenario_Name': 'Customer Risk Level Calculation',
            'Description': 'Calculate risk level based on account balance',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'risk_level',
            'Derivation_Logic': 'CASE WHEN balance > 50000 THEN "LOW" WHEN balance > 10000 THEN "MEDIUM" ELSE "HIGH" END',
        },
        {
            'Scenario_ID': 'TXN_004',
            'Scenario_Name': 'Total Transaction Amount',
            'Description': 'Sum of all transaction amounts per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'total_transaction_amount',
            'Derivation_Logic': 'SUM(amount)',
        },
        {
            'Scenario_ID': 'TXN_005',
            'Scenario_Name': 'Transaction Count',
            'Description': 'Count of transactions per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'transaction_count',
            'Derivation_Logic': 'COUNT(*)',
        },
        {
            'Scenario_ID': 'TXN_006',
            'Scenario_Name': 'Average Transaction Amount',
            'Description': 'Average transaction amount per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'avg_transaction_amount',
            'Derivation_Logic': 'AVG(amount)',
        },
        {
            'Scenario_ID': 'TXN_007',
            'Scenario_Name': 'Account Status Flag',
            'Description': 'Active/Inactive status based on balance',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'account_status',
            'Derivation_Logic': 'CASE WHEN balance > 0 THEN "ACTIVE" ELSE "INACTIVE" END',
        },
        {
            'Scenario_ID': 'TXN_008',
            'Scenario_Name': 'Email Domain Extract',
            'Description': 'Extract domain from customer email address',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'email_domain',
            'Derivation_Logic': 'SUBSTR(email, STRPOS(email, "@") + 1)',
        },
        {
            'Scenario_ID': 'TXN_009',
            'Scenario_Name': 'Customer Age Category',
            'Description': 'Categorize customers by age groups',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'age_category',
            'Derivation_Logic': 'CASE WHEN age < 25 THEN "YOUNG" WHEN age < 50 THEN "MIDDLE" ELSE "SENIOR" END',
        },
        {
            'Scenario_ID': 'TXN_010',
            'Scenario_Name': 'Latest Transaction Date',
            'Description': 'Most recent transaction date per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'latest_transaction_date',
            'Derivation_Logic': 'MAX(transaction_date)',
        }
    ]
    # Main test scenarios data - focused on transformation logic
    test_scenarios = [
        {
            'Scenario_ID': 'TXN_001',
            'Scenario_Name': 'Customer Full Name Transformation',
            'Description': 'Concatenate first name and last name to create full name',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
        },
        {
            'Scenario_ID': 'TXN_002',
            'Scenario_Name': 'Account Balance Copy',
            'Description': 'Direct copy of account balance from source to target',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'account_balance',
            'Derivation_Logic': 'balance',
        },
        {
            'Scenario_ID': 'TXN_003',
            'Scenario_Name': 'Customer Risk Level Calculation',
            'Description': 'Calculate risk level based on account balance',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'risk_level',
            'Derivation_Logic': 'CASE WHEN balance > 50000 THEN "LOW" WHEN balance > 10000 THEN "MEDIUM" ELSE "HIGH" END',
        },
        {
            'Scenario_ID': 'TXN_004',
            'Scenario_Name': 'Total Transaction Amount',
            'Description': 'Sum of all transaction amounts per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'total_transaction_amount',
            'Derivation_Logic': 'SUM(amount)',
        },
        {
            'Scenario_ID': 'TXN_005',
            'Scenario_Name': 'Transaction Count',
            'Description': 'Count of transactions per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'transaction_count',
            'Derivation_Logic': 'COUNT(*)',
        },
        {
            'Scenario_ID': 'TXN_006',
            'Scenario_Name': 'Average Transaction Amount',
            'Description': 'Average transaction amount per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'avg_transaction_amount',
            'Derivation_Logic': 'AVG(amount)',
        },
        {
            'Scenario_ID': 'TXN_007',
            'Scenario_Name': 'Account Status Flag',
            'Description': 'Active/Inactive status based on balance',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'account_status',
            'Derivation_Logic': 'CASE WHEN balance > 0 THEN "ACTIVE" ELSE "INACTIVE" END',
        },
        {
            'Scenario_ID': 'TXN_008',
            'Scenario_Name': 'Email Domain Extract',
            'Description': 'Extract domain from customer email address',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'email_domain',
            'Derivation_Logic': 'SUBSTR(email, STRPOS(email, "@") + 1)',
        },
        {
            'Scenario_ID': 'TXN_009',
            'Scenario_Name': 'Customer Age Category',
            'Description': 'Categorize customers by age groups',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Join_Key': 'customer_id',
            'Target_Column': 'age_category',
            'Derivation_Logic': 'CASE WHEN age < 25 THEN "YOUNG" WHEN age < 50 THEN "MIDDLE" ELSE "SENIOR" END',
        },
        {
            'Scenario_ID': 'TXN_010',
            'Scenario_Name': 'Latest Transaction Date',
            'Description': 'Most recent transaction date per customer',
            'Source_Table': 'transactions',
            'Target_Table': 'customer_summary',
            'Join_Key': 'account_number',
            'Target_Column': 'latest_transaction_date',
            'Derivation_Logic': 'MAX(transaction_date)',
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
    
    # Create Excel file with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'BigQuery_Test_Scenarios_Sample_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main scenarios sheet
        df_scenarios.to_excel(writer, sheet_name='Transformation_Logic', index=False)
        
        # Documentation sheets
        config.to_excel(writer, sheet_name='Configuration', index=False)
        
        # Instructions sheet
        instructions = pd.DataFrame([
            {'Step': 1, 'Action': 'Review Transformation Logic', 'Description': 'Examine the pre-built transformation scenarios in the Transformation_Logic sheet'},
            {'Step': 2, 'Action': 'Understand Derivation Logic', 'Description': 'Review the SQL derivation logic for each target column transformation'},
            {'Step': 3, 'Action': 'Modify Logic', 'Description': 'Update Derivation_Logic column with your specific transformation requirements'},
            {'Step': 4, 'Action': 'Set Target Tables', 'Description': 'Define target table names where transformed data should be validated'},
            {'Step': 5, 'Action': 'Configure Settings', 'Description': 'Update Configuration sheet with your BigQuery project details'},
            {'Step': 6, 'Action': 'Upload to Streamlit', 'Description': 'Use the Excel Scenarios tab to upload this file for validation'},
            {'Step': 7, 'Action': 'Execute Validation', 'Description': 'Run validation to compare source transformations with target table data'},
            {'Step': 8, 'Action': 'Review Results', 'Description': 'Analyze pass/fail results with detailed SQL logic used'},
            {'Step': 9, 'Action': 'Add Custom Transformations', 'Description': 'Create additional rows for your specific transformation scenarios'}
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
                'Join_Key': 'your_join_column',
                'Target_Column': 'column_to_validate',
                'Derivation_Logic': 'SQL expression for transformation (e.g., UPPER(first_name))',
            }
        ])
        custom_template.to_excel(writer, sheet_name='Custom_Template', index=False)
    
    return filename

if __name__ == "__main__":
    filename = create_bigquery_test_scenarios_excel()
    print(f"✅ Transformation Logic Excel file created: {filename}")
    print(f"📍 Location: {os.path.abspath(filename)}")
    print("\n🎯 This file contains:")
    print("  • 10 transformation scenarios with SQL derivation logic")
    print("  • Source-to-target column mapping definitions")
    print("  • Configuration settings for BigQuery project")
    print("  • Step-by-step instructions for validation")
    print("  • Custom transformation template")
    print("\n🚀 Key Features:")
    print("  • Focused on data transformation validation")
    print("  • SQL derivation logic for target column calculations")
    print("  • Pass/fail validation against target table data")
    print("  • Detailed output with SQL logic tracking")
    print("\n📤 Upload this file in the 'Excel Scenarios' tab of your Streamlit app!")
