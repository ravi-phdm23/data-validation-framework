#!/usr/bin/env python3
"""
Test corrected S003 scenario end-to-end
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from test_s003_direct import execute_query_direct

def test_corrected_s003():
    """Test the corrected S003 scenario end-to-end."""
    
    print("🔍 Testing corrected S003 scenario...")
    print("=" * 60)
    
    # Read the new Excel file
    print("Step 1: Reading corrected Excel file...")
    df = pd.read_excel('Multi_Validation_Scenarios_20250728_214744.xlsx')
    s003_data = df[df['Scenario_Name'] == 'S003_Transaction_Status_Validation']
    
    if len(s003_data) == 0:
        print("❌ S003 scenario not found!")
        return
    
    s003_row = s003_data.iloc[0]
    print("✅ Corrected S003 scenario:")
    print(f"  Source Table: {s003_row['Source_Table']}")
    print(f"  Target Table: {s003_row['Target_Table']}")
    print(f"  Source Join Key: {s003_row['Source_Join_Key']}")
    print(f"  Target Join Key: {s003_row['Target_Join_Key']}")
    print(f"  Derivation Logic: {s003_row['Derivation_Logic']}")
    
    # Generate scenario
    print("\nStep 2: Generating scenario object...")
    scenarios = generate_scenarios_from_excel(s003_data, 'cohesive-apogee-411113', 'banking_sample_data')
    scenario = scenarios[0]
    
    # Generate SQL
    print("\nStep 3: Generating SQL...")
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
    
    print("✅ SQL generated successfully")
    
    # Test query execution
    print("\nStep 4: Testing query execution...")
    result = execute_query_direct(sql_query, "s003_validation")
    
    if result['success']:
        print("✅ Query executed successfully!")
        print(f"   Result rows: {result['row_count']}")
        
        if result['row_count'] > 0:
            print("   Validation results:")
            print(result['data'])
        else:
            print("   No rows returned - validation passed!")
    else:
        print("❌ Query execution failed!")
        print(f"   Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("S003 Corrected Test Complete")

if __name__ == "__main__":
    test_corrected_s003()
