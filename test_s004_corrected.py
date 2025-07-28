#!/usr/bin/env python3
"""
Test corrected S004 Customer Balance Category Validation
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from test_s003_direct import execute_query_direct

def test_corrected_s004():
    """Test the corrected S004 scenario end-to-end."""
    
    print("🔍 Testing corrected S004 scenario...")
    print("=" * 70)
    
    # Read the new Excel file
    print("Step 1: Reading corrected Excel file...")
    df = pd.read_excel('Multi_Validation_Scenarios_20250728_215954.xlsx')
    s004_data = df[df['Scenario_Name'] == 'S004_Customer_Balance_Category_Validation']
    
    if len(s004_data) == 0:
        print("❌ S004 scenario not found!")
        return
    
    s004_row = s004_data.iloc[0]
    print("✅ Corrected S004 scenario:")
    print(f"  Source Table: {s004_row['Source_Table']}")
    print(f"  Target Table: {s004_row['Target_Table']}")
    print(f"  Source Join Key: {s004_row['Source_Join_Key']}")
    print(f"  Target Join Key: {s004_row['Target_Join_Key']}")
    print(f"  Target Column: {s004_row['Target_Column']}")
    print(f"  Derivation Logic: {s004_row['Derivation_Logic']}")
    
    # Step 2: Check if tables and columns exist
    print("\\nStep 2: Verifying table and column existence...")
    
    # Check source table and balance column
    source_check = execute_query_direct("SELECT balance FROM cohesive-apogee-411113.banking_sample_data.customers LIMIT 1", "source_balance_check")
    if source_check['success']:
        print("✅ Source table 'customers' exists with 'balance' column")
    else:
        print(f"❌ Issue with source table: {source_check['error']}")
    
    # Check target table
    target_check = execute_query_direct("SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.customer_summary LIMIT 1", "target_check")
    if target_check['success']:
        print("✅ Target table 'customer_summary' exists")
        
        # Check if target column exists
        target_col_check = execute_query_direct("SELECT * FROM cohesive-apogee-411113.banking_sample_data.customer_summary LIMIT 1", "target_columns")
        if target_col_check['success']:
            target_columns = list(target_col_check['data'].columns)
            print(f"📋 Target table columns: {target_columns}")
            if 'customer_tier' in target_columns:
                print("✅ Target column 'customer_tier' exists")
            else:
                print("⚠️ Target column 'customer_tier' may not exist")
                print("💡 Will proceed with test to see what happens")
    else:
        print(f"❌ Issue with target table: {target_check['error']}")
    
    # Generate scenario
    print("\\nStep 3: Generating scenario object...")
    scenarios = generate_scenarios_from_excel(s004_data, 'cohesive-apogee-411113', 'banking_sample_data')
    scenario = scenarios[0]
    
    # Generate SQL
    print("\\nStep 4: Generating SQL...")
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
    
    # Check if balance-based CASE WHEN is preserved
    balance_case_logic = 'CASE WHEN balance < 1000 THEN "Basic" WHEN balance < 10000 THEN "Standard" ELSE "Premium" END'
    if balance_case_logic in sql_query:
        print("✅ Balance categorization logic correctly preserved!")
    elif 'CASE WHEN balance' in sql_query:
        print("⚠️ Balance CASE logic found but may need adjustment")
    else:
        print("❌ Balance categorization logic not properly converted")
    
    print("\\n📝 Generated SQL preview:")
    print("-" * 50)
    lines = sql_query.split('\\n')
    for line in lines[:15]:
        print(line)
    print("... (truncated)")
    print("-" * 50)
    
    # Test query execution
    print("\\nStep 5: Testing query execution...")
    result = execute_query_direct(sql_query, "s004_validation")
    
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
        
        # If target column doesn't exist, suggest alternative
        if "Unrecognized name" in result['error'] and "customer_tier" in result['error']:
            print("\\n💡 The 'customer_tier' column doesn't exist in customer_summary")
            print("   Let me find an alternative column...")
            
            # Check what columns actually exist
            alt_check = execute_query_direct("SELECT * FROM cohesive-apogee-411113.banking_sample_data.customer_summary LIMIT 1", "alt_columns")
            if alt_check['success']:
                cols = list(alt_check['data'].columns)
                print(f"   Available columns: {cols}")
                
                # Look for tier/category/status columns
                tier_cols = [col for col in cols if any(word in col.lower() for word in ['tier', 'category', 'status', 'segment', 'class'])]
                if tier_cols:
                    print(f"   Suggested alternative columns: {tier_cols}")
    
    print("\\n" + "=" * 70)
    print("S004 Corrected Test Complete")

if __name__ == "__main__":
    test_corrected_s004()
