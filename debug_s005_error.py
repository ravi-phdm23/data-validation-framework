import pandas as pd
import os
from sql_generator import create_enhanced_transformation_sql

def test_s005_specifically():
    print("=== Testing S005 Account Type Category Validation ===")
    
    try:
        # Find the latest Excel file
        excel_files = [f for f in os.listdir('.') if f.startswith('Multi_Validation_Scenarios') and f.endswith('.xlsx')]
        if not excel_files:
            print("❌ No Excel files found!")
            return
            
        excel_file = sorted(excel_files)[-1]
        print(f"Using Excel file: {excel_file}")
        
        # Read all scenarios from Sheet1
        df = pd.read_excel(excel_file, sheet_name='Sheet1')
        
        # Filter for S005 scenario
        s005_df = df[df['Scenario_Name'] == 'S005_Account_Type_Category_Validation']
        
        if s005_df.empty:
            print("❌ S005 scenario not found in the Excel file!")
            return
        
        print("✅ S005 scenario found in Excel")
        print("S005 Configuration:")
        print(s005_df[['Source_Table', 'Target_Table', 'Source_Join_Key', 'Target_Join_Key', 'Target_Column', 'Derivation_Logic']].to_string())
        print()

        # Extract configuration from S005 row
        source_table = s005_df.iloc[0]['Source_Table']
        target_table = s005_df.iloc[0]['Target_Table']
        source_join_key = s005_df.iloc[0]['Source_Join_Key']
        target_join_key = s005_df.iloc[0]['Target_Join_Key']
        target_column = s005_df.iloc[0]['Target_Column']
        business_logic = s005_df.iloc[0]['Derivation_Logic']

        print(f"Source Table: {source_table}")
        print(f"Target Table: {target_table}")
        print(f"Source Join Key: {source_join_key}")
        print(f"Target Join Key: {target_join_key}")
        print(f"Target Column: {target_column}")
        print(f"Business Logic: {business_logic}")
        print()

        # Test SQL generation
        print("Generating SQL...")
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
        
        print("✅ SQL generated successfully!")
        print("Generated SQL (first 500 characters):")
        print(sql_query[:500] + "..." if len(sql_query) > 500 else sql_query)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing S005: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_s005_specifically()
