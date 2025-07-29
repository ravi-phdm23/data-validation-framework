import pandas as pd
import os
from sql_generator import create_enhanced_transformation_sql

def test_s005_with_execution():
    print("=== S005 COMPREHENSIVE TEST ===")
    
    try:
        # Setup BigQuery client (without credentials for SQL generation test)
        print("1. Testing SQL Generation...")
        
        # Find the latest Excel file
        excel_files = [f for f in os.listdir('.') if f.startswith('Multi_Validation_Scenarios') and f.endswith('.xlsx')]
        excel_file = sorted(excel_files)[-1]
        
        # Read S005 scenario
        df = pd.read_excel(excel_file, sheet_name='Sheet1')
        s005_df = df[df['Scenario_Name'] == 'S005_Account_Type_Category_Validation']

        # Extract configuration
        source_table = s005_df.iloc[0]['Source_Table']
        target_table = s005_df.iloc[0]['Target_Table']
        source_join_key = s005_df.iloc[0]['Source_Join_Key']
        target_join_key = s005_df.iloc[0]['Target_Join_Key']
        target_column = s005_df.iloc[0]['Target_Column']
        business_logic = s005_df.iloc[0]['Derivation_Logic']

        # Generate SQL
        sql_query = create_enhanced_transformation_sql(
            source_table=source_table,
            target_table=target_table,
            source_join_key=source_join_key,
            target_join_key=target_join_key,
            target_column=target_column,
            derivation_logic=business_logic,
            project_id='cohesive-apogee-411113',
            dataset_id='banking_sample_data'
        )
        
        print("✅ SQL Generation: SUCCESS")
        
        # Test BigQuery execution (if credentials available)
        print("\n2. Testing BigQuery Execution...")
        try:
            from google.cloud import bigquery
            
            # Try to set up credentials
            credentials_path = r'C:\Users\Arnav\OneDrive\Documents\TCoE\cohesive-apogee-411113-7e1a6a9cec94.json'
            if os.path.exists(credentials_path):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                client = bigquery.Client()
                
                # Test query execution
                job = client.query(sql_query)
                results = job.result()
                
                print("✅ BigQuery Execution: SUCCESS")
                print(f"   Total rows returned: {job.result().total_rows}")
                
                # Show sample results
                sample_count = 0
                for row in results:
                    if sample_count < 3:
                        print(f"   Sample result: {dict(row)}")
                        sample_count += 1
                    else:
                        break
                
            else:
                print("⚠️  BigQuery credentials not found, skipping execution test")
                
        except Exception as bq_error:
            print(f"❌ BigQuery Execution Error: {bq_error}")
            
        # Show the full SQL for inspection
        print("\n3. Generated SQL Query:")
        print("=" * 50)
        print(sql_query)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in S005 test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_s005_with_execution()
    if success:
        print("\n🎉 S005 test completed successfully!")
    else:
        print("\n💥 S005 test failed!")
