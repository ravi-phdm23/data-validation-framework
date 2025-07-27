#!/usr/bin/env python3
"""
Create BigQuery Test Scenarios Sample Excel File
This script creates a comprehensive sample Excel file with validation scenarios.
"""

import pandas as pd
from datetime import datetime
import os

def create_sample_excel():
    """Create a comprehensive sample Excel file with BigQuery test scenarios."""
    
    # Sample validation scenarios for banking data
    scenarios_data = {
        'Scenario_Name': [
            'Customer_Balance_Aggregation',
            'Transaction_Count_By_Customer',
            'Average_Transaction_Amount',
            'High_Value_Transaction_Check',
            'Customer_Data_Completeness',
            'Address_Format_Validation',
            'Balance_Range_Validation',
            'Monthly_Transaction_Trends'
        ],
        'Source_Table': [
            'customers',
            'transactions',
            'transactions',
            'transactions',
            'customers',
            'customers',
            'customers',
            'transactions'
        ],
        'Target_Table': [
            'customer_summary',
            'customer_transaction_count',
            'transaction_averages',
            'high_value_alerts',
            'data_quality_report',
            'email_validation_report',
            'balance_audit_report',
            'monthly_trends'
        ],
        'Source_Join_Key': [
            'customer_id',
            'account_number',
            'account_number',
            'transaction_id',
            'customer_id',
            'customer_id',
            'customer_id',
            'account_number'
        ],
        'Target_Join_Key': [
            'cust_id',
            'account_num',
            'account_num',
            'trans_id',
            'cust_id',
            'cust_id',
            'cust_id',
            'account_num'
        ],
        'Target_Column': [
            'total_balance',
            'transaction_count',
            'avg_amount',
            'risk_flag',
            'completeness_score',
            'email_valid',
            'balance_status',
            'monthly_total'
        ],
        'Derivation_Logic': [
            'SUM(balance) GROUP_BY customer_id',
            'COUNT(*) GROUP_BY account_number',
            'AVG(amount) GROUP_BY account_number',  
            'IF(amount > 10000, "High Risk", "Normal")',
            'CHECK_NOT_NULL(customer_id, first_name, address)',
            'VALIDATE_ADDRESS_FORMAT(address)',
            'RANGE_CHECK(balance, min_value=0, max_value=1000000)',
            'SUM(amount) GROUP_BY account_number'
        ],
        'Validation_Type': [
            'Aggregation',
            'Count',
            'Average',
            'Conditional Logic',
            'Data Quality',
            'Format Validation',
            'Range Check',
            'Time Series'
        ],
        'Business_Rule': [
            'Sum all account balances per customer for total wealth calculation',
            'Count number of transactions per account for activity analysis',
            'Calculate average transaction amount per account for spending patterns',
            'Flag high-value transactions above $10,000 for risk management',
            'Ensure all customer records have complete mandatory fields (ID, name, address)',
            'Validate customer addresses have sufficient detail and format',
            'Check account balances are within acceptable range (0 to $1M)',
            'Aggregate monthly transaction volumes for trend analysis'
        ],
        'Expected_Result': [
            'Positive numeric values aggregated by customer',
            'Non-negative integer counts per account',
            'Positive decimal values representing averages',
            'Text values: "High Risk" or "Normal"',
            'Percentage score of data completeness for required fields',
            'Text values: "Valid Address" for complete addresses',
            'Text values: "Within Range", "Below Range", or "Above Range"',
            'Monthly totals aggregated by year-month'
        ],
        'Test_Priority': [
            'High',
            'Medium',
            'Medium',
            'High',
            'Critical',
            'Medium',
            'High',
            'Low'
        ]
    }
    
    # Create DataFrame
    scenarios_df = pd.DataFrame(scenarios_data)
    
    # Create additional sheets for comprehensive sample
    
    # Data Quality Rules sheet
    data_quality_rules = {
        'Rule_ID': ['DQ001', 'DQ002', 'DQ003', 'DQ004', 'DQ005'],
        'Rule_Name': [
            'Customer ID Not Null',
            'Email Format Check',
            'Balance Positive Check',
            'Transaction Date Valid',
            'Account Number Format'
        ],
        'Table_Name': ['customers', 'customers', 'customers', 'transactions', 'customers'],
        'Column_Name': ['customer_id', 'email', 'balance', 'transaction_date', 'account_number'],
        'Rule_Logic': [
            'customer_id IS NOT NULL',
            'email LIKE "%@%.%"',
            'balance >= 0',
            'transaction_date <= CURRENT_DATE()',
            'LENGTH(account_number) = 10'
        ],
        'Severity': ['Critical', 'High', 'High', 'Medium', 'Medium']
    }
    dq_rules_df = pd.DataFrame(data_quality_rules)
    
    # Business Logic Examples sheet
    business_logic_examples = {
        'Category': [
            'Aggregation',
            'Aggregation',
            'Conditional Logic',
            'Data Quality',
            'Format Validation',
            'Range Check',
            'Date Operations',
            'String Operations'
        ],
        'Example_Logic': [
            'SUM(amount) GROUP_BY customer_id',
            'COUNT(*) GROUP_BY account_type',
            'IF(balance > 50000, "Premium", "Standard")',
            'CHECK_NOT_NULL(first_name, last_name, email)',
            'VALIDATE_EMAIL_FORMAT(email)',
            'RANGE_CHECK(age, min_value=18, max_value=100)',
            'DATE_FILTER(transaction_date, last_30_days)',
            'UPPER(first_name) + " " + UPPER(last_name)'
        ],
        'Description': [
            'Sum transaction amounts by customer',
            'Count records by account type',
            'Classify customers based on balance',
            'Check for null values in required fields',
            'Validate email address format',
            'Check if age is within valid range',
            'Filter transactions from last 30 days',
            'Concatenate and uppercase name fields'
        ],
        'Use_Case': [
            'Customer total spending analysis',
            'Account type distribution reporting',
            'Customer segmentation for marketing',
            'Data completeness assessment',
            'Contact information validation',
            'Customer demographic validation',
            'Recent activity analysis',
            'Name standardization for reporting'
        ]
    }
    business_logic_df = pd.DataFrame(business_logic_examples)
    
    # Configuration sheet
    config_data = {
        'Setting': [
            'Project_ID',
            'Dataset_ID',
            'Default_Date_Format',
            'Max_Records_Per_Query',
            'Timeout_Minutes',
            'Log_Level'
        ],
        'Value': [
            'cohesive-apogee-411113',
            'banking_sample_data',
            'YYYY-MM-DD',
            '10000',
            '30',
            'INFO'
        ],
        'Description': [
            'Google Cloud Project ID for BigQuery',
            'BigQuery dataset containing the tables',
            'Standard date format for date comparisons',
            'Maximum number of records to process per query',
            'Query timeout in minutes',
            'Logging level for validation execution'
        ]
    }
    config_df = pd.DataFrame(config_data)
    
    # Create Excel file with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = 'BigQuery_Test_Scenarios_Sample.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main scenarios sheet
        scenarios_df.to_excel(writer, sheet_name='Validation_Scenarios', index=False)
        
        # Additional sheets
        dq_rules_df.to_excel(writer, sheet_name='Data_Quality_Rules', index=False)
        business_logic_df.to_excel(writer, sheet_name='Business_Logic_Examples', index=False)
        config_df.to_excel(writer, sheet_name='Configuration', index=False)
        
        # Add a readme sheet
        readme_data = {
            'Section': [
                'Overview',
                'Validation_Scenarios Sheet',
                'Data_Quality_Rules Sheet',
                'Business_Logic_Examples Sheet',
                'Configuration Sheet',
                'Usage Instructions'
            ],
            'Description': [
                'This Excel file contains sample BigQuery validation scenarios for banking data validation framework.',
                'Main sheet with transformation validation scenarios. Upload this to the Streamlit app to generate BigQuery test scenarios.',
                'Additional data quality rules that can be converted to validation scenarios.',
                'Examples of business logic patterns that can be used in the Derivation_Logic column.',
                'Configuration settings for the BigQuery connection and validation parameters.',
                'Upload the Validation_Scenarios sheet to the Streamlit app, select it, and click "Generate BigQuery Scenarios from Mapping".'
            ]
        }
        readme_df = pd.DataFrame(readme_data)
        readme_df.to_excel(writer, sheet_name='README', index=False)
    
    print(f"✅ Created sample Excel file: {filename}")
    print(f"📋 File contains {len(scenarios_df)} validation scenarios")
    print("📁 Sheets created:")
    print("   - Validation_Scenarios (main scenarios)")
    print("   - Data_Quality_Rules (additional rules)")
    print("   - Business_Logic_Examples (logic patterns)")
    print("   - Configuration (settings)")
    print("   - README (instructions)")
    
    return filename

if __name__ == "__main__":
    create_sample_excel()
