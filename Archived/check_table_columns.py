from google.cloud import bigquery
import os

# Set up BigQuery client
try:
    credentials_path = r'C:\Users\Arnav\OneDrive\Documents\TCoE\cohesive-apogee-411113-7e1a6a9cec94.json'
    if os.path.exists(credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    
    client = bigquery.Client()
    
    # Check account_profiles table structure
    print("=== Checking account_profiles table structure ===")
    query = """
    SELECT column_name, data_type 
    FROM `cohesive-apogee-411113.banking_sample_data.INFORMATION_SCHEMA.COLUMNS` 
    WHERE table_name = 'account_profiles'
    ORDER BY ordinal_position
    """
    
    results = client.query(query).result()
    
    print("Columns in account_profiles:")
    columns = []
    for row in results:
        columns.append(row.column_name)
        print(f"  - {row.column_name} ({row.data_type})")
    
    print(f"\nTotal columns: {len(columns)}")
    
    # Check if account_type exists
    if 'account_type' in columns:
        print("✅ account_type column EXISTS in account_profiles")
    else:
        print("❌ account_type column DOES NOT EXIST in account_profiles")
        print("Available columns:", columns)
        
        # Look for similar columns
        similar_cols = [col for col in columns if 'type' in col.lower() or 'account' in col.lower()]
        if similar_cols:
            print(f"Similar columns found: {similar_cols}")
    
    # Also check account_type_summary table
    print("\n=== Checking account_type_summary table structure ===")
    query2 = """
    SELECT column_name, data_type 
    FROM `cohesive-apogee-411113.banking_sample_data.INFORMATION_SCHEMA.COLUMNS` 
    WHERE table_name = 'account_type_summary'
    ORDER BY ordinal_position
    """
    
    results2 = client.query(query2).result()
    
    print("Columns in account_type_summary:")
    target_columns = []
    for row in results2:
        target_columns.append(row.column_name)
        print(f"  - {row.column_name} ({row.data_type})")
    
    print(f"\nTotal columns: {len(target_columns)}")
    
    # Sample data from both tables
    print("\n=== Sample data from account_profiles (first 3 rows) ===")
    sample_query = "SELECT * FROM `cohesive-apogee-411113.banking_sample_data.account_profiles` LIMIT 3"
    sample_results = client.query(sample_query).result()
    
    for i, row in enumerate(sample_results):
        print(f"Row {i+1}: {dict(row)}")
    
    print("\n=== Sample data from account_type_summary (first 3 rows) ===")
    sample_query2 = "SELECT * FROM `cohesive-apogee-411113.banking_sample_data.account_type_summary` LIMIT 3"
    sample_results2 = client.query(sample_query2).result()
    
    for i, row in enumerate(sample_results2):
        print(f"Row {i+1}: {dict(row)}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
