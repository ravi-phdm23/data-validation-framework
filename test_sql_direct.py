#!/usr/bin/env python3
"""
Simple test script to test SQL generation and execution for the scenario
"""

import pandas as pd
from bigquery_client import connect_to_bigquery, execute_custom_query
from sql_generator import create_enhanced_transformation_sql

def test_sql_generation():
    """Test SQL generation and execution directly"""
    
    print("Testing BigQuery connection...")
    try:
        client = connect_to_bigquery('cohesive-apogee-411113', 'banking_sample_data')
        if client:
            print("✅ BigQuery connection successful")
        else:
            print("❌ BigQuery connection failed")
            return
    except Exception as e:
        print(f"❌ BigQuery connection error: {e}")
        return
    
    # Test the specific scenario manually
    print("\nTesting SQL generation...")
    try:
        sql_query = create_enhanced_transformation_sql(
            source_table='customers',
            target_table='customer_summary',
            source_join_key='customer_id',
            target_join_key='cust_id',
            target_column='calculated_full_name',
            derivation_logic='CONCAT(first_name, " ", last_name)',
            project_id='cohesive-apogee-411113',
            dataset_id='banking_sample_data'
        )
        
        if sql_query:
            print("✅ SQL generated successfully:")
            print("=" * 80)
            print(sql_query)
            print("=" * 80)
        else:
            print("❌ Failed to generate SQL")
            return
            
    except Exception as e:
        print(f"❌ Error generating SQL: {e}")
        import traceback
        print(traceback.format_exc())
        return
    
    print("\nExecuting query...")
    try:
        result, message = execute_custom_query(sql_query, 'S001_Customer_Full_Name_Validation')
        
        print(f"Result status: {result.get('status') if result else 'None'}")
        print(f"Message: {message}")
        
        if result and result['status'] == 'success':
            df_result = result['data']
            print(f"✅ Query executed successfully")
            print(f"   Rows returned: {len(df_result) if df_result is not None else 0}")
            if df_result is not None and not df_result.empty:
                print("   Sample results:")
                print(df_result.head())
                print("\n   Column info:")
                print(f"   Columns: {df_result.columns.tolist()}")
                
                # Check validation result
                if 'validation_result' in df_result.columns:
                    passed_count = len(df_result[df_result['validation_result'] == 'PASS'])
                    total_count = len(df_result)
                    status = 'PASS' if passed_count == total_count else 'FAIL'
                    print(f"   Validation Status: {status}")
                    print(f"   Passed: {passed_count}/{total_count}")
                else:
                    print("   No validation_result column found")
                    print("   Assuming FAIL if rows returned (indicating discrepancies)")
                    status = 'FAIL' if len(df_result) > 0 else 'PASS'
                    print(f"   Inferred Status: {status}")
            else:
                print("   No data returned - likely indicates PASS (no discrepancies found)")
                
        elif result and result['status'] == 'error':
            print(f"❌ Query failed: {result.get('error', 'Unknown error')}")
        else:
            print("❌ Unexpected result format")
            
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_sql_generation()
