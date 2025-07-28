#!/usr/bin/env python3
"""
BigQuery Dataset Explorer
Explore the cohesive-apogee-411113.banking_sample_data dataset structure
"""

from google.cloud import bigquery
import pandas as pd
import os

def explore_dataset():
    """Explore the banking_sample_data dataset structure."""
    
    project_id = "cohesive-apogee-411113"
    dataset_id = "banking_sample_data"
    
    print(f"🔍 Exploring BigQuery Dataset: {project_id}.{dataset_id}")
    print("=" * 60)
    
    try:
        # Initialize BigQuery client
        client = bigquery.Client(project=project_id)
        
        # Get dataset reference
        dataset_ref = client.dataset(dataset_id)
        dataset = client.get_dataset(dataset_ref)
        
        print(f"📊 Dataset: {dataset.dataset_id}")
        print(f"📅 Created: {dataset.created}")
        print(f"📍 Location: {dataset.location}")
        print()
        
        # List all tables in the dataset
        tables = list(client.list_tables(dataset))
        
        if not tables:
            print("❗ No tables found in the dataset")
            return
        
        print(f"📋 Found {len(tables)} tables:")
        print("-" * 40)
        
        for table in tables:
            print(f"📄 Table: {table.table_id}")
            
            # Get table details
            table_ref = dataset_ref.table(table.table_id)
            table_obj = client.get_table(table_ref)
            
            print(f"   Rows: {table_obj.num_rows:,}")
            print(f"   Size: {table_obj.num_bytes / (1024*1024):.2f} MB")
            print(f"   Columns: {len(table_obj.schema)}")
            
            # Show schema
            print("   Schema:")
            for field in table_obj.schema:
                print(f"     - {field.name}: {field.field_type} {'(NULLABLE)' if field.mode == 'NULLABLE' else '(REQUIRED)'}")
            
            # Sample data
            print("   Sample Data (first 5 rows):")
            query = f"""
            SELECT * 
            FROM `{project_id}.{dataset_id}.{table.table_id}` 
            LIMIT 5
            """
            
            try:
                results = client.query(query).to_dataframe()
                if not results.empty:
                    for idx, row in results.iterrows():
                        print(f"     Row {idx + 1}: {dict(row)}")
                else:
                    print("     No data found")
            except Exception as e:
                print(f"     Error reading sample data: {str(e)}")
            
            print()
    
    except Exception as e:
        print(f"❌ Error exploring dataset: {str(e)}")
        print("💡 Make sure you have:")
        print("   1. BigQuery credentials configured")
        print("   2. Access to the cohesive-apogee-411113 project")
        print("   3. google-cloud-bigquery package installed")

if __name__ == "__main__":
    explore_dataset()
