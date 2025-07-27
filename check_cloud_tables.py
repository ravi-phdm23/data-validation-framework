#!/usr/bin/env python3
"""
Check BigQuery Cloud Tables
Verify if reference tables were created successfully in the cloud.
"""

from google.cloud import bigquery
import sys

def check_cloud_tables():
    """Check if reference tables exist in BigQuery cloud."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print(f"🔍 Checking tables in {project_id}.{dataset_id}...")
        print("=" * 60)
        
        # List all tables in the dataset
        tables = list(client.list_tables(f"{project_id}.{dataset_id}"))
        
        if not tables:
            print("❌ No tables found in the dataset!")
            return False
        
        print(f"📋 Found {len(tables)} tables in the dataset:")
        
        reference_tables = ['interest_rates', 'fee_structure', 'risk_categories', 'customer_tiers', 'product_categories', 'customer_activity', 'credit_limits', 'compliance_rules', 'product_matrix']
        found_reference_tables = []
        
        for table in tables:
            is_reference = "🆕" if table.table_id in reference_tables else "📊"
            print(f"  {is_reference} {table.table_id}")
            if table.table_id in reference_tables:
                found_reference_tables.append(table.table_id)
        
        print("\n" + "=" * 60)
        
        # Check specific reference tables
        if found_reference_tables:
            print(f"✅ Reference tables found: {', '.join(found_reference_tables)}")
            
            # Query each reference table to show data
            for table_name in found_reference_tables:
                print(f"\n🔍 Data in {table_name}:")
                print("-" * 40)
                
                query = f"""
                SELECT *
                FROM `{project_id}.{dataset_id}.{table_name}`
                ORDER BY 1
                """
                
                job = client.query(query)
                results = job.result()
                
                row_count = 0
                for row in results:
                    row_count += 1
                    row_data = [str(value) for value in row.values()]
                    print(f"  Row {row_count}: {' | '.join(row_data)}")
                
                if row_count == 0:
                    print("  (No data found)")
                else:
                    print(f"  Total rows: {row_count}")
        else:
            print("❌ Reference tables (interest_rates, fee_structure) not found!")
            
        # Test a simple query to verify cloud connectivity
        print(f"\n🧪 Testing cloud connectivity...")
        test_query = f"""
        SELECT COUNT(*) as total_customers
        FROM `{project_id}.{dataset_id}.customers`
        """
        
        job = client.query(test_query)
        result = list(job.result())[0]
        print(f"✅ Cloud connection verified - {result.total_customers} customers in main table")
        
        return len(found_reference_tables) > 0
        
    except Exception as e:
        print(f"❌ Error checking cloud tables: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_cloud_tables()
    sys.exit(0 if success else 1)
