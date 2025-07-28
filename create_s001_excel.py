#!/usr/bin/env python3
"""
Create Excel file for Scenario S001: Customer Full Name Validation
"""

import pandas as pd
from datetime import datetime

def create_scenario_s001_excel():
    """Create Excel file for the first test scenario."""
    
    print("📝 Creating Excel file for Scenario S001...")
    
    # Define the scenario data
    scenario_data = {
        'scenario_id': ['S001'],
        'scenario_name': ['Customer Full Name Validation'],
        'description': ['Validate full name calculation from first and last name'],
        'expected_result': ['Should PASS if calculated names match existing names'],
        'project_id': ['cohesive-apogee-411113'],
        'dataset_id': ['banking_sample_data'],
        'source_table': ['customers'],
        'target_table': ['customer_summary'],
        'source_join_key': ['customer_id'],
        'target_join_key': ['cust_id'],
        'target_column': ['calculated_full_name'],
        'derivation_logic': ['CONCAT(first_name, " ", last_name)'],
        'reference_table': [''],
        'reference_join_key': [''],
        'reference_lookup_column': [''],
        'reference_return_column': [''],
        'created_date': [datetime.now().strftime('%Y-%m-%d')],
        'created_by': ['validation_framework'],
        'status': ['READY_TO_TEST']
    }
    
    # Create DataFrame
    df = pd.DataFrame(scenario_data)
    
    # Save to Excel
    filename = 'Scenario_S001_Customer_Name_Validation.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main scenario sheet
        df.to_excel(writer, sheet_name='Validation_Scenarios', index=False)
        
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
                'How to use:',
                '1. Run: python run_app.py',
                '2. Go to "📊 Excel Scenario Validation" tab',
                '3. Upload this Excel file',
                '4. Click "Execute All Scenarios"',
                '',
                f'Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                'Project: cohesive-apogee-411113.banking_sample_data'
            ]
        }
        
        info_df = pd.DataFrame(info_data)
        info_df.to_excel(writer, sheet_name='Test_Info', index=False)
    
    print(f"✅ Created: {filename}")
    print("\n🧪 Scenario S001 Details:")
    print("=" * 40)
    print("📊 Source: customers → Target: customer_summary")
    print("🔧 Logic: CONCAT(first_name, ' ', last_name)")
    print("🎯 Tests: Full name calculation accuracy")
    print("\n🚀 Ready to test in Streamlit app!")
    
    return filename

if __name__ == "__main__":
    create_scenario_s001_excel()
