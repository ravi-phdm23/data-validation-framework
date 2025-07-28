#!/usr/bin/env python3
"""
Debug S005 Account Type Reference Validation specifically
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql, create_reference_table_validation_sql
from test_s003_direct import execute_query_direct
import traceback

def debug_s005():
    """Debug the S005 scenario step by step."""
    
    print("🔍 Debugging S005_Account_Type_Reference_Validation...")
    print("=" * 70)
    
    try:
        # Step 1: Read the Excel file
        print("Step 1: Reading Excel file...")
        df = pd.read_excel('Multi_Validation_Scenarios_20250728_220138.xlsx')
        print(f"✅ Excel file loaded with {len(df)} rows")
        
        # Step 2: Filter S005 scenario
        print("\nStep 2: Filtering S005 scenario...")
        s005_data = df[df['Scenario_Name'] == 'S005_Account_Type_Reference_Validation']
        
        if len(s005_data) == 0:
            print("❌ S005 scenario not found!")
            return
        
        s005_row = s005_data.iloc[0]
        print("✅ S005 scenario found:")
        print(f"  Source Table: {s005_row['Source_Table']}")
        print(f"  Target Table: {s005_row['Target_Table']}")
        print(f"  Source Join Key: {s005_row['Source_Join_Key']}")
        print(f"  Target Join Key: {s005_row['Target_Join_Key']}")
        print(f"  Target Column: {s005_row['Target_Column']}")
        print(f"  Derivation Logic: {s005_row['Derivation_Logic']}")
        print(f"  Reference Table: {s005_row['Reference_Table']}")
        print(f"  Reference Join Key: {s005_row['Reference_Join_Key']}")
        print(f"  Reference Lookup Column: {s005_row['Reference_Lookup_Column']}")
        print(f"  Reference Return Column: {s005_row['Reference_Return_Column']}")
        
        # Step 3: Check table existence
        print("\nStep 3: Checking table existence...")
        
        # Check source table
        try:
            source_check = execute_query_direct(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s005_row['Source_Table']} LIMIT 1", "source_check")
            if source_check['success']:
                print(f"✅ Source table '{s005_row['Source_Table']}' exists")
                
                # Check source columns
                source_col_check = execute_query_direct(f"SELECT * FROM cohesive-apogee-411113.banking_sample_data.{s005_row['Source_Table']} LIMIT 1", "source_columns")
                if source_col_check['success']:
                    source_columns = list(source_col_check['data'].columns)
                    print(f"📋 Source table columns: {source_columns}")
                    
                    # Check if derivation logic column exists
                    derivation_col = s005_row['Derivation_Logic']
                    if derivation_col in source_columns:
                        print(f"✅ Derivation column '{derivation_col}' found")
                    else:
                        print(f"❌ Derivation column '{derivation_col}' NOT found")
            else:
                print(f"❌ Source table '{s005_row['Source_Table']}' doesn't exist")
                print(f"   Error: {source_check['error']}")
        except Exception as e:
            print(f"❌ Error checking source table: {str(e)}")
            
        # Check target table
        try:
            target_check = execute_query_direct(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s005_row['Target_Table']} LIMIT 1", "target_check")
            if target_check['success']:
                print(f"✅ Target table '{s005_row['Target_Table']}' exists")
                
                # Check target columns
                target_col_check = execute_query_direct(f"SELECT * FROM cohesive-apogee-411113.banking_sample_data.{s005_row['Target_Table']} LIMIT 1", "target_columns")
                if target_col_check['success']:
                    target_columns = list(target_col_check['data'].columns)
                    print(f"📋 Target table columns: {target_columns}")
                    if s005_row['Target_Column'] in target_columns:
                        print(f"✅ Target column '{s005_row['Target_Column']}' found")
                    else:
                        print(f"❌ Target column '{s005_row['Target_Column']}' NOT found")
            else:
                print(f"❌ Target table '{s005_row['Target_Table']}' doesn't exist")
                print(f"   Error: {target_check['error']}")
        except Exception as e:
            print(f"❌ Error checking target table: {str(e)}")
        
        # Check reference table
        try:
            ref_check = execute_query_direct(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s005_row['Reference_Table']} LIMIT 1", "ref_check")
            if ref_check['success']:
                print(f"✅ Reference table '{s005_row['Reference_Table']}' exists")
                
                # Check reference columns
                ref_col_check = execute_query_direct(f"SELECT * FROM cohesive-apogee-411113.banking_sample_data.{s005_row['Reference_Table']} LIMIT 1", "ref_columns")
                if ref_col_check['success']:
                    ref_columns = list(ref_col_check['data'].columns)
                    print(f"📋 Reference table columns: {ref_columns}")
                    
                    lookup_col = s005_row['Reference_Lookup_Column']
                    return_col = s005_row['Reference_Return_Column']
                    
                    if lookup_col in ref_columns:
                        print(f"✅ Reference lookup column '{lookup_col}' found")
                    else:
                        print(f"❌ Reference lookup column '{lookup_col}' NOT found")
                        
                    if return_col in ref_columns:
                        print(f"✅ Reference return column '{return_col}' found")
                    else:
                        print(f"❌ Reference return column '{return_col}' NOT found")
            else:
                print(f"❌ Reference table '{s005_row['Reference_Table']}' doesn't exist")
                print(f"   Error: {ref_check['error']}")
        except Exception as e:
            print(f"❌ Error checking reference table: {str(e)}")
        
        # Step 4: List available account/type tables
        print("\nStep 4: Finding account/type related tables...")
        try:
            tables_result = execute_query_direct("SELECT table_name FROM cohesive-apogee-411113.banking_sample_data.INFORMATION_SCHEMA.TABLES ORDER BY table_name", "list_tables")
            if tables_result['success']:
                all_tables = tables_result['data']['table_name'].tolist()
                
                # Look for account-related tables
                account_tables = [t for t in all_tables if 'account' in t.lower()]
                print(f"🔍 Account-related tables found:")
                for table in account_tables:
                    print(f"  ✅ {table}")
                
                # Look for type/reference tables
                type_tables = [t for t in all_tables if 'type' in t.lower() or 'ref' in t.lower() or 'lookup' in t.lower()]
                print(f"🔍 Type/Reference tables found:")
                for table in type_tables:
                    print(f"  ✅ {table}")
                    
        except Exception as e:
            print(f"❌ Error listing tables: {str(e)}")
        
        # Step 5: Test scenario generation
        print("\nStep 5: Testing scenario generation...")
        scenarios = generate_scenarios_from_excel(s005_data, 'cohesive-apogee-411113', 'banking_sample_data')
        
        if not scenarios:
            print("❌ No scenarios generated!")
            return
            
        scenario = scenarios[0]
        print("✅ Scenario object generated:")
        print(f"  Name: {scenario['scenario_name']}")
        print(f"  Source: {scenario['source_table']}")
        print(f"  Target: {scenario['target_table']}")
        print(f"  Reference: {scenario['reference_table']}")
        print(f"  Has Reference Table: {bool(scenario.get('reference_table') and str(scenario.get('reference_table')).lower() not in ['nan', 'none', ''])}")
        
        # Step 6: Test SQL generation
        print("\nStep 6: Testing SQL generation...")
        
        # Check if this is a reference table scenario
        has_reference = scenario.get('reference_table') and str(scenario.get('reference_table')).lower() not in ['nan', 'none', '']
        
        if has_reference:
            print("🔗 Using reference table validation SQL...")
            sql_query = create_reference_table_validation_sql(
                source_table=scenario['source_table'],
                target_table=scenario['target_table'], 
                source_join_key=scenario['source_join_key'],
                target_join_key=scenario['target_join_key'],
                target_column=scenario['target_column'],
                derivation_logic=scenario['derivation_logic'],
                reference_table=scenario['reference_table'],
                reference_join_key=scenario['reference_join_key'],
                reference_lookup_column=scenario['reference_lookup_column'],
                reference_return_column=scenario['reference_return_column'],
                project_id='cohesive-apogee-411113',
                dataset_id='banking_sample_data'
            )
        else:
            print("📝 Using standard transformation SQL...")
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
            lines = sql_query.split('\n')
            for i, line in enumerate(lines[:20]):
                print(line)
            if len(lines) > 20:
                print("... (truncated)")
            print("-" * 50)
        else:
            print("❌ SQL generation failed")
        
        # Step 7: Test query execution if all tables exist
        if sql_query:
            print("\nStep 7: Testing query execution...")
            result = execute_query_direct(sql_query, "s005_test")
            
            if result['success']:
                print("✅ Query executed successfully!")
                print(f"   Rows returned: {result['row_count']}")
                
                if result['row_count'] > 0:
                    print("   Sample results:")
                    print(result['data'].head())
            else:
                print("❌ Query execution failed!")
                print(f"   Error: {result['error']}")
                
                # Analyze the error to suggest fixes
                if "was not found" in result['error']:
                    print("💡 Table or column not found - need to update scenario configuration")
                elif "Unrecognized name" in result['error']:
                    print("💡 Column name issue - need to verify column names")
        
    except Exception as e:
        print(f"❌ Error during S005 debugging: {str(e)}")
        traceback.print_exc()
        
    print("\n" + "=" * 70)
    print("S005 Debug Complete")

if __name__ == "__main__":
    debug_s005()
