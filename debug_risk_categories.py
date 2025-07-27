#!/usr/bin/env python3
"""
Debug Risk Categories Structure
Check the structure and data types in risk_categories table.
"""

from google.cloud import bigquery

def debug_risk_categories():
    """Debug the risk_categories table structure and join issues."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print("🔍 Debugging risk_categories table structure...")
        
        # Check table schema
        table_ref = client.get_table(f"{project_id}.{dataset_id}.risk_categories")
        print(f"\n📋 Schema for risk_categories:")
        for field in table_ref.schema:
            print(f"  - {field.name}: {field.field_type}")
        
        # Check data types in customers table for balance
        customers_ref = client.get_table(f"{project_id}.{dataset_id}.customers")
        print(f"\n📋 Relevant fields in customers table:")
        for field in customers_ref.schema:
            if 'balance' in field.name.lower() or 'risk' in field.name.lower():
                print(f"  - {field.name}: {field.field_type}")
        
        # Check actual data and types
        print(f"\n🔍 Sample data from risk_categories:")
        query = f"""
        SELECT 
            balance_range,
            min_balance,
            max_balance,
            risk_score,
            TYPEOF(balance_range) as balance_range_type,
            TYPEOF(min_balance) as min_balance_type
        FROM `{project_id}.{dataset_id}.risk_categories`
        ORDER BY min_balance
        """
        
        job = client.query(query)
        results = job.result()
        
        for row in results:
            print(f"  {row.balance_range} ({row.balance_range_type}): min={row.min_balance} ({row.min_balance_type}), max={row.max_balance}, score={row.risk_score}")
        
        # Check customers balance data type
        print(f"\n🔍 Sample customers data types:")
        query = f"""
        SELECT 
            customer_id,
            balance,
            TYPEOF(balance) as balance_type,
            TYPEOF(customer_id) as customer_id_type
        FROM `{project_id}.{dataset_id}.customers`
        WHERE balance > 0
        LIMIT 3
        """
        
        job = client.query(query)
        results = job.result()
        
        for row in results:
            print(f"  Customer {row.customer_id} ({row.customer_id_type}): balance={row.balance} ({row.balance_type})")
        
        # Show the problematic join scenario
        print(f"\n❌ The Issue:")
        print(f"  - risk_categories.balance_range is STRING (e.g., 'LOW', 'MEDIUM')")
        print(f"  - customers.balance is FLOAT64 (numeric)")
        print(f"  - The join condition 'balance = balance_range' compares STRING with FLOAT64")
        
        print(f"\n✅ The Solution:")
        print(f"  - Use CASE WHEN logic to categorize balance into ranges")
        print(f"  - Then join on the categorized balance_range")
        
        return True
        
    except Exception as e:
        print(f"❌ Error debugging risk categories: {str(e)}")
        return False

if __name__ == "__main__":
    debug_risk_categories()
