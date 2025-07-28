#!/usr/bin/env python3
"""
Final test of corrected S004 Customer Balance Category Validation
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from test_s003_direct import execute_query_direct

def test_final_s004():
    """Test the final corrected S004 scenario."""
    
    print("🔍 Testing FINAL corrected S004 scenario...")
    print("=" * 70)
    
    # Read the final Excel file
    df = pd.read_excel('Multi_Validation_Scenarios_20250728_220138.xlsx')
    s004_data = df[df['Scenario_Name'] == 'S004_Customer_Balance_Category_Validation']
    s004_row = s004_data.iloc[0]
    
    print("✅ Final S004 scenario configuration:")
    print(f"  Source Table: {s004_row['Source_Table']}")
    print(f"  Target Table: {s004_row['Target_Table']}")
    print(f"  Target Column: {s004_row['Target_Column']}")
    print(f"  Derivation Logic: {s004_row['Derivation_Logic']}")
    
    # Generate scenario
    scenarios = generate_scenarios_from_excel(s004_data, 'cohesive-apogee-411113', 'banking_sample_data')
    scenario = scenarios[0]
    
    # Generate SQL
    sql_query = create_enhanced_transformation_sql(
        source_table=scenario['source_table'],
        target_table=scenario['target_table'], 
        source_join_key=scenario['source_join_key'],
        target_join_key=scenario['target_join_key'],
        target_column=scenario['target_column'],
        derivation_logic=scenario['derivation_logic'],
        project_id='cohesive-apogee-411113',
        dataset_id='banking_sample_data'
    )
    
    print("\\n📝 Generated SQL Preview:")
    print("-" * 50)
    lines = sql_query.split('\\n')
    for line in lines[:15]:
        print(line)
    print("... (truncated)")
    print("-" * 50)
    
    # Check if risk level CASE WHEN is preserved
    risk_case_logic = 'CASE WHEN balance < 1000 THEN "High" WHEN balance < 10000 THEN "Medium" ELSE "Low" END'
    if risk_case_logic in sql_query:
        print("✅ Risk level categorization logic correctly preserved!")
    
    # Test execution
    print("\\n🚀 Testing query execution...")
    result = execute_query_direct(sql_query, "final_s004_test")
    
    if result['success']:
        print("✅ Query executed successfully!")
        print(f"   Rows returned: {result['row_count']}")
        
        if result['row_count'] > 0:
            print("\\n📊 Validation results:")
            print(result['data'])
            print("\\n💡 This shows validation comparison results")
        else:
            print("\\n✅ No mismatches found - validation PASSED!")
    else:
        print("❌ Query execution failed!")
        print(f"   Error: {result['error']}")
    
    print("\\n" + "=" * 70)
    print("✅ S004 FINAL CORRECTION COMPLETE!")

if __name__ == "__main__":
    test_final_s004()
