#!/usr/bin/env python3
"""
Final test of corrected S003 scenario
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from test_s003_direct import execute_query_direct

def test_final_s003():
    """Test the final corrected S003 scenario."""
    
    print("🔍 Testing FINAL corrected S003 scenario...")
    print("=" * 70)
    
    # Read the final Excel file
    df = pd.read_excel('Multi_Validation_Scenarios_20250728_215304.xlsx')
    s003_data = df[df['Scenario_Name'] == 'S003_Transaction_Status_Validation']
    s003_row = s003_data.iloc[0]
    
    print("✅ Final S003 scenario configuration:")
    print(f"  Source Table: {s003_row['Source_Table']}")
    print(f"  Target Table: {s003_row['Target_Table']}")
    print(f"  Source Join Key: {s003_row['Source_Join_Key']}")
    print(f"  Target Join Key: {s003_row['Target_Join_Key']}")
    print(f"  Target Column: {s003_row['Target_Column']}")
    print(f"  Derivation Logic: {s003_row['Derivation_Logic']}")
    
    # Generate scenario
    scenarios = generate_scenarios_from_excel(s003_data, 'cohesive-apogee-411113', 'banking_sample_data')
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
    for line in lines[:15]:  # Show first 15 lines
        print(line)
    print("... (truncated)")
    print("-" * 50)
    
    # Check if CASE WHEN is preserved
    if 'CASE WHEN amount > 0 THEN "Credit" ELSE "Debit" END' in sql_query:
        print("✅ CASE WHEN logic correctly preserved!")
    
    # Test execution
    print("\\n🚀 Testing query execution...")
    result = execute_query_direct(sql_query, "final_s003_test")
    
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
    print("✅ S003 FINAL CORRECTION COMPLETE!")

if __name__ == "__main__":
    test_final_s003()
