#!/usr/bin/env python3
"""
Test Enhanced Reference Table Features
Create sample reference tables and test VLOOKUP scenarios.
"""

import pandas as pd
from google.cloud import bigquery
import logging

def create_sample_reference_tables():
    """Create sample reference tables in BigQuery for testing enhanced features."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print("🔄 Creating sample reference tables...")
        
        # 1. Interest Rates Reference Table
        interest_rates_data = [
            {'account_type': 'SAVINGS', 'rate_value': 0.025, 'description': 'Standard Savings Rate'},
            {'account_type': 'CHECKING', 'rate_value': 0.01, 'description': 'Basic Checking Rate'},
            {'account_type': 'PREMIUM', 'rate_value': 0.045, 'description': 'Premium Account Rate'},
            {'account_type': 'BUSINESS', 'rate_value': 0.035, 'description': 'Business Account Rate'}
        ]
        
        interest_rates_df = pd.DataFrame(interest_rates_data)
        
        # Create table in BigQuery
        table_id = f"{project_id}.{dataset_id}.interest_rates"
        
        # Define schema
        schema = [
            bigquery.SchemaField("account_type", "STRING"),
            bigquery.SchemaField("rate_value", "FLOAT64"),
            bigquery.SchemaField("description", "STRING"),
        ]
        
        # Create table
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        
        # Load data
        job = client.load_table_from_dataframe(interest_rates_df, table)
        job.result()  # Wait for job to complete
        
        print(f"✅ Created interest_rates table with {len(interest_rates_data)} rows")
        
        # 2. Fee Structure Reference Table
        fee_structure_data = [
            {'transaction_type': 'TRANSFER', 'fee_percentage': 0.001, 'min_fee': 1.0, 'max_fee': 50.0},
            {'transaction_type': 'WITHDRAWAL', 'fee_percentage': 0.002, 'min_fee': 2.0, 'max_fee': 25.0},
            {'transaction_type': 'DEPOSIT', 'fee_percentage': 0.0, 'min_fee': 0.0, 'max_fee': 0.0},
            {'transaction_type': 'PAYMENT', 'fee_percentage': 0.0015, 'min_fee': 1.5, 'max_fee': 75.0}
        ]
        
        fee_structure_df = pd.DataFrame(fee_structure_data)
        
        # Create table in BigQuery
        table_id = f"{project_id}.{dataset_id}.fee_structure"
        
        # Define schema
        schema = [
            bigquery.SchemaField("transaction_type", "STRING"),
            bigquery.SchemaField("fee_percentage", "FLOAT64"),
            bigquery.SchemaField("min_fee", "FLOAT64"),
            bigquery.SchemaField("max_fee", "FLOAT64"),
        ]
        
        # Create table
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        
        # Load data
        job = client.load_table_from_dataframe(fee_structure_df, table)
        job.result()  # Wait for job to complete
        
        print(f"✅ Created fee_structure table with {len(fee_structure_data)} rows")
        
        # 3. Test VLOOKUP scenario directly
        print("\n🧪 Testing VLOOKUP functionality...")
        
        vlookup_query = f"""
        -- VLOOKUP Test: Get interest rates for customer account types
        SELECT 
            c.customer_id,
            c.account_type,
            c.balance,
            r.rate_value as applicable_rate,
            c.balance * r.rate_value as annual_interest
        FROM `{project_id}.{dataset_id}.customers` c
        LEFT JOIN `{project_id}.{dataset_id}.interest_rates` r
            ON c.account_type = r.account_type
        ORDER BY c.customer_id
        LIMIT 10
        """
        
        job = client.query(vlookup_query)
        results = job.result()
        
        print("VLOOKUP Results:")
        for row in results:
            rate_pct = row.applicable_rate * 100 if row.applicable_rate else 0
            interest = row.annual_interest if row.annual_interest else 0
            print(f"Customer {row.customer_id}: {row.account_type} account, Balance: ${row.balance:,.2f}, Rate: {rate_pct:.1f}%, Annual Interest: ${interest:,.2f}")
        
        # 4. Test conditional logic
        print("\n🧪 Testing Conditional Logic...")
        
        conditional_query = f"""
        -- Conditional Logic Test: Customer tier classification
        SELECT 
            customer_id,
            balance,
            CASE 
                WHEN balance > 100000 THEN 'PREMIUM'
                WHEN balance > 50000 THEN 'GOLD'
                ELSE 'STANDARD'
            END as customer_tier,
            CASE 
                WHEN balance > 100000 THEN 'VIP Service'
                WHEN balance > 50000 THEN 'Priority Service'
                ELSE 'Regular Service'
            END as service_level
        FROM `{project_id}.{dataset_id}.customers`
        ORDER BY balance DESC
        LIMIT 10
        """
        
        job = client.query(conditional_query)
        results = job.result()
        
        print("Conditional Logic Results:")
        for row in results:
            print(f"Customer {row.customer_id}: Balance ${row.balance:,.2f} → {row.customer_tier} tier ({row.service_level})")
        
        print("\n✅ Enhanced reference table features are working correctly!")
        print("🎯 You can now test these scenarios in the Streamlit application:")
        print("   1. Upload the Enhanced_BigQuery_Validation_Scenarios_*.xlsx file")
        print("   2. Select the 'Enhanced_Scenarios' worksheet")
        print("   3. Generate and execute scenarios with VLOOKUP and conditional logic")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating reference tables: {str(e)}")
        return False

if __name__ == "__main__":
    create_sample_reference_tables()
