#!/usr/bin/env python3
"""
Debug S002 Account Balance Validation specifically
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from bigquery_client import execute_custom_query
import traceback

def debug_s002():
    """Debug the S002 scenario step by step."""
    
    print("🔍 Debugging S002_Account_Balance_Validation...")
    print("=" * 60)
    
    try:
        # Step 1: Read the Excel file
        print("Step 1: Reading Excel file...")
        df = pd.read_excel('Multi_Validation_Scenarios_20250728_210632.xlsx')
        print(f"✅ Excel file loaded with {len(df)} rows")
        
        # Step 2: Filter S002 scenario
        print("\nStep 2: Filtering S002 scenario...")
        s002_data = df[df['Scenario_Name'] == 'S002_Account_Balance_Validation']
        
        if len(s002_data) == 0:
            print("❌ S002 scenario not found!")
            return
        
        s002_row = s002_data.iloc[0]
        print("✅ S002 scenario found:")
        print(f"  Source Table: {s002_row['Source_Table']}")
        print(f"  Target Table: {s002_row['Target_Table']}")
        print(f"  Source Join Key: {s002_row['Source_Join_Key']}")
        print(f"  Target Join Key: {s002_row['Target_Join_Key']}")
        print(f"  Target Column: {s002_row['Target_Column']}")
        print(f"  Derivation Logic: {s002_row['Derivation_Logic']}")
        
        # Step 3: Generate scenario object
        print("\nStep 3: Generating scenario object...")
        scenarios = generate_scenarios_from_excel(s002_data, 'cohesive-apogee-411113', 'banking_sample_data')
        
        if not scenarios:
            print("❌ No scenarios generated!")
            return
            
        scenario = scenarios[0]
        print("✅ Scenario object generated:")
        print(f"  Name: {scenario['scenario_name']}")
        print(f"  Source: {scenario['source_table']}")
        print(f"  Target: {scenario['target_table']}")
        print(f"  Derivation: {scenario['derivation_logic']}")
        
        # Step 4: Generate SQL
        print("\nStep 4: Generating SQL query...")
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
        
        if not sql_query:
            print("❌ SQL generation failed!")
            return
            
        print("✅ SQL query generated:")
        print("-" * 40)
        print(sql_query)
        print("-" * 40)
        
        # Step 5: Check table existence first
        print("\nStep 5: Checking table existence...")
        
        # Check source table
        source_check = execute_custom_query(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{scenario['source_table']} LIMIT 1")
        if source_check and 'data' in source_check:
            print(f"✅ Source table '{scenario['source_table']}' exists")
        else:
            print(f"❌ Source table '{scenario['source_table']}' doesn't exist or not accessible")
            print(f"   Result: {source_check}")
            
        # Check target table
        target_check = execute_custom_query(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{scenario['target_table']} LIMIT 1")
        if target_check and 'data' in target_check:
            print(f"✅ Target table '{scenario['target_table']}' exists")
        else:
            print(f"❌ Target table '{scenario['target_table']}' doesn't exist or not accessible")
            print(f"   Result: {target_check}")
        
        # Step 6: Execute the validation query
        print("\nStep 6: Executing validation query...")
        result = execute_custom_query(sql_query)
        
        if result and 'data' in result:
            print("✅ Query executed successfully!")
            print(f"   Result rows: {len(result['data'])}")
            
            if len(result['data']) > 0:
                print("   Sample results:")
                print(result['data'].head())
                print("\n   This typically indicates validation FAILURES")
            else:
                print("   No rows returned - this typically indicates validation PASS")
        else:
            print("❌ Query execution failed!")
            print(f"   Result: {result}")
        
    except Exception as e:
        print(f"❌ Error during debugging: {str(e)}")
        traceback.print_exc()
        
    print("\n" + "=" * 60)
    print("S002 Debug Complete")

if __name__ == "__main__":
    debug_s002()
