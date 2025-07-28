#!/usr/bin/env python3
"""
Debug S004 Customer Age Category Validation specifically
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from test_s003_direct import execute_query_direct
import traceback

def debug_s004():
    """Debug the S004 scenario step by step."""
    
    print("🔍 Debugging S004_Customer_Age_Category_Validation...")
    print("=" * 70)
    
    try:
        # Step 1: Read the Excel file
        print("Step 1: Reading Excel file...")
        df = pd.read_excel('Multi_Validation_Scenarios_20250728_215304.xlsx')
        print(f"✅ Excel file loaded with {len(df)} rows")
        
        # Step 2: Filter S004 scenario
        print("\nStep 2: Filtering S004 scenario...")
        s004_data = df[df['Scenario_Name'] == 'S004_Customer_Age_Category_Validation']
        
        if len(s004_data) == 0:
            print("❌ S004 scenario not found!")
            return
        
        s004_row = s004_data.iloc[0]
        print("✅ S004 scenario found:")
        print(f"  Source Table: {s004_row['Source_Table']}")
        print(f"  Target Table: {s004_row['Target_Table']}")
        print(f"  Source Join Key: {s004_row['Source_Join_Key']}")
        print(f"  Target Join Key: {s004_row['Target_Join_Key']}")
        print(f"  Target Column: {s004_row['Target_Column']}")
        print(f"  Derivation Logic: {s004_row['Derivation_Logic']}")
        
        # Step 3: Check table existence
        print("\nStep 3: Checking table existence...")
        
        # Check source table
        try:
            source_check = execute_query_direct(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s004_row['Source_Table']} LIMIT 1", "source_check")
            if source_check['success']:
                print(f"✅ Source table '{s004_row['Source_Table']}' exists")
                
                # Check for age column
                age_check = execute_query_direct(f"SELECT * FROM cohesive-apogee-411113.banking_sample_data.{s004_row['Source_Table']} LIMIT 1", "age_check")
                if age_check['success']:
                    columns = list(age_check['data'].columns)
                    print(f"📋 Source table columns: {columns}")
                    if 'age' in columns:
                        print("✅ 'age' column found in source table")
                    else:
                        print("❌ 'age' column NOT found in source table")
                        print("💡 Need to find an alternative age-related column")
            else:
                print(f"❌ Source table '{s004_row['Source_Table']}' doesn't exist")
                print(f"   Error: {source_check['error']}")
        except Exception as e:
            print(f"❌ Error checking source table: {str(e)}")
            
        # Check target table
        try:
            target_check = execute_query_direct(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s004_row['Target_Table']} LIMIT 1", "target_check")
            if target_check['success']:
                print(f"✅ Target table '{s004_row['Target_Table']}' exists")
                
                # Check target columns
                target_col_check = execute_query_direct(f"SELECT * FROM cohesive-apogee-411113.banking_sample_data.{s004_row['Target_Table']} LIMIT 1", "target_col_check")
                if target_col_check['success']:
                    target_columns = list(target_col_check['data'].columns)
                    print(f"📋 Target table columns: {target_columns}")
                    if s004_row['Target_Column'] in target_columns:
                        print(f"✅ Target column '{s004_row['Target_Column']}' found")
                    else:
                        print(f"❌ Target column '{s004_row['Target_Column']}' NOT found")
            else:
                print(f"❌ Target table '{s004_row['Target_Table']}' doesn't exist")
                print(f"   Error: {target_check['error']}")
        except Exception as e:
            print(f"❌ Error checking target table: {str(e)}")
        
        # Step 4: List available tables to find alternatives
        print("\nStep 4: Finding customer/demographic tables...")
        try:
            tables_result = execute_query_direct("SELECT table_name FROM cohesive-apogee-411113.banking_sample_data.INFORMATION_SCHEMA.TABLES ORDER BY table_name", "list_tables")
            if tables_result['success']:
                all_tables = tables_result['data']['table_name'].tolist()
                
                # Look for customer-related tables
                customer_tables = [t for t in all_tables if 'customer' in t.lower()]
                print(f"🔍 Customer-related tables found:")
                for table in customer_tables:
                    print(f"  ✅ {table}")
                
                # Look for demographic tables
                demo_tables = [t for t in all_tables if 'demo' in t.lower() or 'age' in t.lower()]
                if demo_tables:
                    print(f"🔍 Demographic-related tables found:")
                    for table in demo_tables:
                        print(f"  ✅ {table}")
                else:
                    print("📋 No demographic-specific tables found")
                    
        except Exception as e:
            print(f"❌ Error listing tables: {str(e)}")
        
        # Step 5: Test SQL generation with current config
        print("\nStep 5: Testing SQL generation...")
        scenarios = generate_scenarios_from_excel(s004_data, 'cohesive-apogee-411113', 'banking_sample_data')
        
        if not scenarios:
            print("❌ No scenarios generated!")
            return
            
        scenario = scenarios[0]
        print("✅ Scenario object generated:")
        print(f"  Name: {scenario['scenario_name']}")
        print(f"  Source: {scenario['source_table']}")
        print(f"  Target: {scenario['target_table']}")
        print(f"  Derivation: {scenario['derivation_logic']}")
        
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
        
        if sql_query:
            print("✅ SQL query generated successfully")
            print("📝 Generated SQL preview:")
            print("-" * 50)
            # Show key parts of the SQL
            lines = sql_query.split('\n')
            for i, line in enumerate(lines[:20]):
                print(line)
            if len(lines) > 20:
                print("... (truncated)")
            print("-" * 50)
            
            # Check if the CASE WHEN age logic is properly generated
            age_case_logic = 'CASE WHEN age < 25 THEN "Young" WHEN age < 65 THEN "Adult" ELSE "Senior" END'
            if age_case_logic in sql_query:
                print("✅ Age categorization logic correctly preserved!")
            elif 'CASE WHEN' in sql_query and 'age' in sql_query:
                print("⚠️ Age CASE logic found but may need adjustment")
            else:
                print("❌ Age categorization logic not properly converted")
        else:
            print("❌ SQL generation failed")
        
        # Step 6: Test query execution if possible
        if sql_query and '✅' in str(source_check.get('success', False)) and '✅' in str(target_check.get('success', False)):
            print("\nStep 6: Testing query execution...")
            result = execute_query_direct(sql_query, "s004_test")
            
            if result['success']:
                print("✅ Query executed successfully!")
                print(f"   Rows returned: {result['row_count']}")
                
                if result['row_count'] > 0:
                    print("   Sample results:")
                    print(result['data'].head())
            else:
                print("❌ Query execution failed!")
                print(f"   Error: {result['error']}")
        
    except Exception as e:
        print(f"❌ Error during S004 debugging: {str(e)}")
        traceback.print_exc()
        
    print("\n" + "=" * 70)
    print("S004 Debug Complete")

if __name__ == "__main__":
    debug_s004()
