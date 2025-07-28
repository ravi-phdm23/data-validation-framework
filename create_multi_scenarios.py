#!/usr/bin/env python3
"""
Create an enhanced Excel file with multiple validation scenarios
"""

import pandas as pd
from datetime import datetime

def create_multi_scenario_excel():
    """Create Excel file with multiple validation scenarios."""
    
    # Define multiple validation scenarios
    scenarios = [
        {
            'Scenario_Name': 'S001_Customer_Full_Name_Validation',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_id',
            'Target_Column': 'calculated_full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
            'Reference_Table': '',
            'Reference_Join_Key': '',
            'Reference_Lookup_Column': '',
            'Reference_Return_Column': '',
            'Business_Conditions': '',
            'Hardcoded_Values': '',
            'Description': 'Validate full name calculation from first and last name',
            'Expected_Result': 'Should PASS if calculated names match existing names'
        },
        {
            'Scenario_Name': 'S002_Account_Balance_Validation',
            'Source_Table': 'account_profiles',
            'Target_Table': 'account_summary_target',
            'Source_Join_Key': 'customer_reference',
            'Target_Join_Key': 'cust_id',
            'Target_Column': 'balance_total',
            'Derivation_Logic': 'current_balance',
            'Reference_Table': '',
            'Reference_Join_Key': '',
            'Reference_Lookup_Column': '',
            'Reference_Return_Column': '',
            'Business_Conditions': '',
            'Hardcoded_Values': '',
            'Description': 'Validate balance total matches current balance from account profiles',
            'Expected_Result': 'Should PASS if balance_total equals current_balance'
        },
        {
            'Scenario_Name': 'S003_Transaction_Status_Validation',
            'Source_Table': 'transactions',
            'Target_Table': 'transaction_summary',
            'Source_Join_Key': 'transaction_id',
            'Target_Join_Key': 'trans_id',
            'Target_Column': 'status_description',
            'Derivation_Logic': 'CASE WHEN amount > 0 THEN "Credit" ELSE "Debit" END',
            'Reference_Table': '',
            'Reference_Join_Key': '',
            'Reference_Lookup_Column': '',
            'Reference_Return_Column': '',
            'Business_Conditions': '',
            'Hardcoded_Values': '',
            'Description': 'Validate transaction status based on amount',
            'Expected_Result': 'Should PASS if status matches amount sign'
        },
        {
            'Scenario_Name': 'S004_Customer_Age_Category_Validation',
            'Source_Table': 'customers',
            'Target_Table': 'customer_demographics',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_id',
            'Target_Column': 'age_category',
            'Derivation_Logic': 'CASE WHEN age < 25 THEN "Young" WHEN age < 65 THEN "Adult" ELSE "Senior" END',
            'Reference_Table': '',
            'Reference_Join_Key': '',
            'Reference_Lookup_Column': '',
            'Reference_Return_Column': '',
            'Business_Conditions': '',
            'Hardcoded_Values': '',
            'Description': 'Validate age category classification',
            'Expected_Result': 'Should PASS if age categories are correctly assigned'
        },
        {
            'Scenario_Name': 'S005_Account_Type_Reference_Validation',
            'Source_Table': 'accounts',
            'Target_Table': 'account_details',
            'Source_Join_Key': 'account_id',
            'Target_Join_Key': 'acc_id',
            'Target_Column': 'account_type_name',
            'Derivation_Logic': 'account_type_code',
            'Reference_Table': 'account_types',
            'Reference_Join_Key': 'type_code',
            'Reference_Lookup_Column': 'type_code',
            'Reference_Return_Column': 'type_name',
            'Business_Conditions': '',
            'Hardcoded_Values': '',
            'Description': 'Validate account type name lookup from reference table',
            'Expected_Result': 'Should PASS if account type names match reference table'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(scenarios)
    
    # Save to Excel file
    filename = f'Multi_Validation_Scenarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"Created Excel file: {filename}")
    print(f"Number of scenarios: {len(scenarios)}")
    print("\nScenarios created:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['Scenario_Name']} - {scenario['Description']}")
    
    return filename

if __name__ == "__main__":
    create_multi_scenario_excel()
