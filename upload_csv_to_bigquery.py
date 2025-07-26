#!/usr/bin/env python3
"""
Simple CSV upload to BigQuery
Project ID: cohesive-apogee-411113
"""

from google.cloud import bigquery
import pandas as pd

def upload_csv_to_bigquery():
    """Upload CSV files directly to BigQuery."""
    
    # Initialize BigQuery client
    client = bigquery.Client(project="cohesive-apogee-411113")
    
    # Dataset and table configuration
    dataset_id = "banking_sample_data"
    customer_table_id = "customers"
    transaction_table_id = "transactions"
    
    print(f"Creating dataset: {dataset_id}")
    
    # Create dataset
    dataset = bigquery.Dataset(f"cohesive-apogee-411113.{dataset_id}")
    dataset.location = "US"
    
    try:
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {dataset.dataset_id}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"Dataset {dataset_id} already exists")
        else:
            print(f"Error creating dataset: {e}")
            return False
    
    # Upload customers CSV
    print("Uploading customer data from CSV...")
    
    customer_table_ref = client.dataset(dataset_id).table(customer_table_id)
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
    )
    
    with open("sample_customers.csv", "rb") as source_file:
        job = client.load_table_from_file(source_file, customer_table_ref, job_config=job_config)
    
    job.result()  # Wait for the job to complete
    
    print(f"Uploaded customer data successfully")
    
    # Upload transactions CSV
    print("Uploading transaction data from CSV...")
    
    transaction_table_ref = client.dataset(dataset_id).table(transaction_table_id)
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
    )
    
    with open("sample_transactions.csv", "rb") as source_file:
        job = client.load_table_from_file(source_file, transaction_table_ref, job_config=job_config)
    
    job.result()  # Wait for the job to complete
    
    print(f"Uploaded transaction data successfully")
    
    # Test the uploaded data
    print("Testing uploaded data...")
    
    # Test customer data
    query = f"""
    SELECT 
        account_type,
        COUNT(*) as count,
        AVG(balance) as avg_balance
    FROM `cohesive-apogee-411113.{dataset_id}.{customer_table_id}`
    GROUP BY account_type
    ORDER BY count DESC
    """
    
    print("Customer data summary:")
    query_job = client.query(query)
    results = query_job.result()
    
    for row in results:
        print(f"  {row.account_type}: {row.count} accounts, avg balance: ${row.avg_balance:.2f}")
    
    # Test transaction data
    query = f"""
    SELECT 
        transaction_type,
        COUNT(*) as count,
        SUM(amount) as total_amount
    FROM `cohesive-apogee-411113.{dataset_id}.{transaction_table_id}`
    GROUP BY transaction_type
    ORDER BY count DESC
    """
    
    print("Transaction data summary:")
    query_job = client.query(query)
    results = query_job.result()
    
    for row in results:
        print(f"  {row.transaction_type}: {row.count} transactions, total: ${row.total_amount:.2f}")
    
    # Test join between tables
    query = f"""
    SELECT COUNT(*) as matching_records
    FROM `cohesive-apogee-411113.{dataset_id}.{customer_table_id}` c
    JOIN `cohesive-apogee-411113.{dataset_id}.{transaction_table_id}` t
    ON c.account_number = t.account_number
    """
    
    print("Cross-table validation:")
    query_job = client.query(query)
    results = query_job.result()
    
    for row in results:
        print(f"  Customer-Transaction matches: {row.matching_records}")
    
    print("Data upload and validation completed successfully!")
    print(f"Your BigQuery tables:")
    print(f"   - cohesive-apogee-411113.{dataset_id}.{customer_table_id}")
    print(f"   - cohesive-apogee-411113.{dataset_id}.{transaction_table_id}")
    
    return True

if __name__ == "__main__":
    upload_csv_to_bigquery()
