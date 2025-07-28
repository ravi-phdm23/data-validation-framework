import pandas as pd
from google.cloud import bigquery
import os
from sql_generator import create_enhanced_transformation_sql

# Set up BigQuery client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\Arnav\OneDrive\Documents\TCoE\cohesive-apogee-411113-7e1a6a9cec94.json'
client = bigquery.Client()

# Read the updated Excel file
excel_file = 'enhanced_validation_mapping_20250725_215659.xlsx'
if not os.path.exists(excel_file):
    # Check for any Excel files
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if excel_files:
        excel_file = excel_files[-1]  # Use the most recent one
        print(f"Using Excel file: {excel_file}")
    else:
        print("No Excel files found!")
        exit()

# Read S005 scenario
df = pd.read_excel(excel_file, sheet_name='S005_Account_Type_Category_Validation')
print("S005 Scenario Configuration:")
print(df.to_string())
print()

# Extract configuration from first row
source_table = df.iloc[0]['source_table']
target_table = df.iloc[0]['target_table']
source_join_key = df.iloc[0]['source_join_key']
target_join_key = df.iloc[0]['target_join_key']
target_column = df.iloc[0]['target_column']
business_logic = df.iloc[0]['derivation_logic']

print(f"Source Table: {source_table}")
print(f"Target Table: {target_table}")
print(f"Source Join Key: {source_join_key}")
print(f"Target Join Key: {target_join_key}")
print(f"Target Column: {target_column}")
print(f"Business Logic: {business_logic}")
print()

try:
    # Generate and test SQL
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
    
    # Test execution
    print("Testing SQL execution...")
    job = client.query(sql_query)
    results = job.result()
    
    print("Query executed successfully!")
    print(f"Number of rows returned: {job.result().total_rows}")
    
    # Show sample results
    for i, row in enumerate(results):
        if i < 3:  # Show first 3 rows
            print(f"Row {i+1}: {dict(row)}")
        else:
            break
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
