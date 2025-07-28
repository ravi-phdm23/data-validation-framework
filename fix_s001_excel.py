#!/usr/bin/env python3
"""
Create correctly formatted Excel file for Scenario S001
"""

import pandas as pd
from datetime import datetime

def create_correct_s001_excel():
    """Create Excel file with the correct column names expected by the app."""
    
    print("📝 Creating correctly formatted Excel file for Scenario S001...")
    
    # Define the scenario data with CORRECT column names
    scenario_data = {
        'Scenario_Name': ['S001_Customer_Full_Name_Validation'],
        'Source_Table': ['customers'],
        'Target_Table': ['customer_summary'],
        'Source_Join_Key': ['customer_id'],
        'Target_Join_Key': ['cust_id'],
        'Target_Column': ['calculated_full_name'],
        'Derivation_Logic': ['CONCAT(first_name, " ", last_name)'],
        'Reference_Table': [''],
        'Reference_Join_Key': [''],
        'Reference_Lookup_Column': [''],
        'Reference_Return_Column': [''],
        'Business_Conditions': [''],
        'Hardcoded_Values': [''],
        'Description': ['Validate full name calculation from first and last name'],
        'Expected_Result': ['Should PASS if calculated names match existing names']
    }
    
    # Create DataFrame
    df = pd.DataFrame(scenario_data)
    
    # Save to Excel
    filename = 'S001_Customer_Name_Validation.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main scenario sheet with correct format
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        
        # Create info sheet
        info_data = {
            'Test Information': [
                'Scenario S001: Customer Full Name Validation',
                '',
                'What this tests:',
                '- Source: customers table (first_name + last_name)',
                '- Target: customer_summary table (calculated_full_name)',
                '- Logic: CONCAT(first_name, " ", last_name)',
                '',
                'Expected Results:',
                '- PASS: If all calculated names match target names',
                '- FAIL: If there are mismatches (shows details)',
                '',
                'Project: cohesive-apogee-411113',
                'Dataset: banking_sample_data',
                '',
                f'Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            ]
        }
        
        info_df = pd.DataFrame(info_data)
        info_df.to_excel(writer, sheet_name='Info', index=False)
    
    print(f"✅ Created: {filename}")
    print("\n📋 Correct Column Format:")
    print("=" * 40)
    for col in df.columns:
        print(f"✓ {col}")
    
    print("\n🧪 Scenario S001 Details:")
    print("=" * 40)
    print("📊 Source: customers → Target: customer_summary") 
    print("🔧 Logic: CONCAT(first_name, ' ', last_name)")
    print("🎯 Tests: Full name calculation accuracy")
    print("\n🚀 Ready to test in Streamlit app!")
    
    return filename

if __name__ == "__main__":
    create_correct_s001_excel()
