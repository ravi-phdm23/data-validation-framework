#!/usr/bin/env python3
"""
Debug S003 Transaction Status Validation specifically
"""

import pandas as pd
from excel_handler import generate_scenarios_from_excel
from sql_generator import create_enhanced_transformation_sql
from bigquery_client import execute_custom_query
import traceback

def debug_s003():
    """Debug the S003 scenario step by step."""
    
    print("🔍 Debugging S003_Transaction_Status_Validation...")
    print("=" * 70)
    
    try:
        # Step 1: Read the Excel file
        print("Step 1: Reading Excel file...")
        df = pd.read_excel('Multi_Validation_Scenarios_20250728_210632.xlsx')
        print(f"✅ Excel file loaded with {len(df)} rows")
        
        # Step 2: Filter S003 scenario
        print("\nStep 2: Filtering S003 scenario...")
        s003_data = df[df['Scenario_Name'] == 'S003_Transaction_Status_Validation']
        
        if len(s003_data) == 0:
            print("❌ S003 scenario not found!")
            return
        
        s003_row = s003_data.iloc[0]
        print("✅ S003 scenario found:")
        print(f"  Source Table: {s003_row['Source_Table']}")
        print(f"  Target Table: {s003_row['Target_Table']}")
        print(f"  Source Join Key: {s003_row['Source_Join_Key']}")
        print(f"  Target Join Key: {s003_row['Target_Join_Key']}")
        print(f"  Target Column: {s003_row['Target_Column']}")
        print(f"  Derivation Logic: {s003_row['Derivation_Logic']}")
        
        # Step 3: Check if tables exist
        print("\nStep 3: Checking table existence...")
        
        # Check source table
        try:
            source_check = execute_custom_query(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s003_row['Source_Table']} LIMIT 1", "source_check")
            if source_check and 'data' in source_check:
                print(f"✅ Source table '{s003_row['Source_Table']}' exists")
            else:
                print(f"❌ Source table '{s003_row['Source_Table']}' doesn't exist")
                print("   Need to identify correct source table name")
        except Exception as e:
            print(f"❌ Error checking source table: {str(e)}")
            
        # Check target table
        try:
            target_check = execute_custom_query(f"SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.{s003_row['Target_Table']} LIMIT 1", "target_check")
            if target_check and 'data' in target_check:
                print(f"✅ Target table '{s003_row['Target_Table']}' exists")
            else:
                print(f"❌ Target table '{s003_row['Target_Table']}' doesn't exist")
                print("   Need to identify correct target table name")
        except Exception as e:
            print(f"❌ Error checking target table: {str(e)}")
        
        # Step 4: List available tables to find correct ones
        print("\nStep 4: Finding available tables...")
        try:
            tables_result = execute_custom_query("SELECT table_name FROM cohesive-apogee-411113.banking_sample_data.INFORMATION_SCHEMA.TABLES ORDER BY table_name", "list_tables")
            if tables_result and 'data' in tables_result:
                all_tables = tables_result['data']['table_name'].tolist()
                print(f"✅ Found {len(all_tables)} tables in dataset")
                
                # Look for transaction-related tables
                transaction_tables = [t for t in all_tables if 'transaction' in t.lower()]
                print(f"\n🔍 Transaction-related tables found:")
                for table in transaction_tables:
                    print(f"  ✅ {table}")
                
                if not transaction_tables:
                    print("  ❌ No transaction-related tables found")
                else:
                    # Use the first transaction table as source
                    correct_source = transaction_tables[0]
                    print(f"\n💡 Suggested correction: Use '{correct_source}' as source table")
                    
                    # Look for summary tables
                    summary_tables = [t for t in all_tables if 'summary' in t.lower()]
                    if summary_tables:
                        print(f"📋 Available summary tables:")
                        for table in summary_tables:
                            print(f"  ✅ {table}")
                        
                        # Check if there's a transaction summary table
                        transaction_summary = [t for t in summary_tables if 'transaction' in t.lower()]
                        if transaction_summary:
                            correct_target = transaction_summary[0]
                            print(f"💡 Suggested target table: '{correct_target}'")
                        else:
                            print("💡 No transaction summary table found, may need to create mock scenario")
                    
        except Exception as e:
            print(f"❌ Error listing tables: {str(e)}")
        
        # Step 5: Generate scenario with original data
        print("\nStep 5: Testing original scenario generation...")
        scenarios = generate_scenarios_from_excel(s003_data, 'cohesive-apogee-411113', 'banking_sample_data')
        
        if not scenarios:
            print("❌ No scenarios generated!")
            return
            
        scenario = scenarios[0]
        print("✅ Scenario object generated:")
        print(f"  Name: {scenario['scenario_name']}")
        print(f"  Source: {scenario['source_table']}")
        print(f"  Target: {scenario['target_table']}")
        print(f"  Derivation: {scenario['derivation_logic']}")
        
        # Step 6: Generate SQL to see if derivation logic is properly handled
        print("\nStep 6: Testing SQL generation...")
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
            # Show just the key part of the SQL
            lines = sql_query.split('\n')
            for i, line in enumerate(lines[:20]):  # Show first 20 lines
                print(line)
            if len(lines) > 20:
                print("... (truncated)")
            print("-" * 50)
            
            # Check if the CASE WHEN logic is properly generated
            if 'CASE WHEN amount > 0 THEN "Credit" ELSE "Debit" END' in sql_query:
                print("✅ Derivation logic correctly converted to SQL")
            elif 'CASE WHEN' in sql_query:
                print("⚠️ CASE WHEN found but may need adjustment")
            else:
                print("❌ Derivation logic not properly converted")
        else:
            print("❌ SQL generation failed")
        
    except Exception as e:
        print(f"❌ Error during S003 debugging: {str(e)}")
        traceback.print_exc()
        
    print("\n" + "=" * 70)
    print("S003 Debug Complete")

if __name__ == "__main__":
    debug_s003()
