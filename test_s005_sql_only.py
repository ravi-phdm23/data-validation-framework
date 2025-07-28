import pandas as pd
import os
from sql_generator import create_enhanced_transformation_sql

# Read the updated Excel file
excel_file = 'Multi_Validation_Scenarios_20250728_220959.xlsx'
if not os.path.exists(excel_file):
    # Check for any Excel files with Multi_Validation pattern
    excel_files = [f for f in os.listdir('.') if f.startswith('Multi_Validation_Scenarios') and f.endswith('.xlsx')]
    if excel_files:
        excel_file = sorted(excel_files)[-1]  # Use the most recent one
        print(f"Using Excel file: {excel_file}")
    else:
        print("No Multi_Validation_Scenarios Excel files found!")
        exit()

try:
    # Read all scenarios from Sheet1
    df = pd.read_excel(excel_file, sheet_name='Sheet1')
    
    # Filter for S005 scenario
    s005_df = df[df['Scenario_Name'] == 'S005_Account_Type_Category_Validation']
    
    if s005_df.empty:
        print("S005 scenario not found in the Excel file!")
        exit()
    
    print("S005 Scenario Configuration:")
    print(s005_df.to_string())
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
    
    print("Generated SQL Query:")
    print(sql_query)
    print()
    print("SQL generation successful for S005!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
