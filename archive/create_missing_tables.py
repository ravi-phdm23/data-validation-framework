#!/usr/bin/env python3
"""
Create Missing Reference Tables
Create all reference tables needed for the enhanced scenarios.
"""

import pandas as pd
from google.cloud import bigquery
import logging

def create_missing_reference_tables():
    """Create all missing reference tables needed for enhanced scenarios."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print("🔄 Creating missing reference tables...")
        
        # 1. Risk Categories Reference Table
        risk_categories_data = [
            {'balance_range': 'LOW', 'min_balance': 0, 'max_balance': 10000, 'risk_score': 1, 'risk_description': 'Low Risk - Small Balance'},
            {'balance_range': 'MEDIUM', 'min_balance': 10001, 'max_balance': 50000, 'risk_score': 3, 'risk_description': 'Medium Risk - Moderate Balance'},
            {'balance_range': 'HIGH', 'min_balance': 50001, 'max_balance': 100000, 'risk_score': 5, 'risk_description': 'High Risk - Large Balance'},
            {'balance_range': 'PREMIUM', 'min_balance': 100001, 'max_balance': 999999999, 'risk_score': 8, 'risk_description': 'Premium Risk - Very Large Balance'}
        ]
        
        risk_categories_df = pd.DataFrame(risk_categories_data)
        
        # Create table in BigQuery
        table_id = f"{project_id}.{dataset_id}.risk_categories"
        
        # Define schema
        schema = [
            bigquery.SchemaField("balance_range", "STRING"),
            bigquery.SchemaField("min_balance", "INT64"),
            bigquery.SchemaField("max_balance", "INT64"),
            bigquery.SchemaField("risk_score", "INT64"),
            bigquery.SchemaField("risk_description", "STRING"),
        ]
        
        # Create table
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        
        # Load data
        job = client.load_table_from_dataframe(risk_categories_df, table)
        job.result()  # Wait for job to complete
        
        print(f"✅ Created risk_categories table with {len(risk_categories_data)} rows")
        
        # 2. Customer Tiers Reference Table
        customer_tiers_data = [
            {'tier_name': 'BRONZE', 'min_balance': 0, 'max_balance': 25000, 'benefits': 'Basic Banking', 'fee_waiver': False},
            {'tier_name': 'SILVER', 'min_balance': 25001, 'max_balance': 75000, 'benefits': 'Priority Support', 'fee_waiver': True},
            {'tier_name': 'GOLD', 'min_balance': 75001, 'max_balance': 150000, 'benefits': 'Premium Services', 'fee_waiver': True},
            {'tier_name': 'PLATINUM', 'min_balance': 150001, 'max_balance': 999999999, 'benefits': 'VIP Treatment', 'fee_waiver': True}
        ]
        
        customer_tiers_df = pd.DataFrame(customer_tiers_data)
        
        # Create table in BigQuery
        table_id = f"{project_id}.{dataset_id}.customer_tiers"
        
        # Define schema
        schema = [
            bigquery.SchemaField("tier_name", "STRING"),
            bigquery.SchemaField("min_balance", "INT64"),
            bigquery.SchemaField("max_balance", "INT64"),
            bigquery.SchemaField("benefits", "STRING"),
            bigquery.SchemaField("fee_waiver", "BOOLEAN"),
        ]
        
        # Create table
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        
        # Load data
        job = client.load_table_from_dataframe(customer_tiers_df, table)
        job.result()  # Wait for job to complete
        
        print(f"✅ Created customer_tiers table with {len(customer_tiers_data)} rows")
        
        # 3. Product Categories Reference Table
        product_categories_data = [
            {'account_type': 'SAVINGS', 'category': 'DEPOSIT', 'product_family': 'Personal Banking', 'min_opening_balance': 100},
            {'account_type': 'CHECKING', 'category': 'TRANSACTIONAL', 'product_family': 'Personal Banking', 'min_opening_balance': 25},
            {'account_type': 'CREDIT', 'category': 'LENDING', 'product_family': 'Credit Products', 'min_opening_balance': 0},
            {'account_type': 'INVESTMENT', 'category': 'INVESTMENT', 'product_family': 'Wealth Management', 'min_opening_balance': 5000},
            {'account_type': 'BUSINESS', 'category': 'COMMERCIAL', 'product_family': 'Business Banking', 'min_opening_balance': 1000},
            {'account_type': 'LOAN', 'category': 'LENDING', 'product_family': 'Credit Products', 'min_opening_balance': 0},
            {'account_type': 'PREMIUM', 'category': 'PREMIUM', 'product_family': 'Private Banking', 'min_opening_balance': 100000}
        ]
        
        product_categories_df = pd.DataFrame(product_categories_data)
        
        # Create table in BigQuery
        table_id = f"{project_id}.{dataset_id}.product_categories"
        
        # Define schema
        schema = [
            bigquery.SchemaField("account_type", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("product_family", "STRING"),
            bigquery.SchemaField("min_opening_balance", "INT64"),
        ]
        
        # Create table
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        
        # Load data
        job = client.load_table_from_dataframe(product_categories_df, table)
        job.result()  # Wait for job to complete
        
        print(f"✅ Created product_categories table with {len(product_categories_data)} rows")
        
        # 4. Test the risk_categories table specifically
        print("\n🧪 Testing risk_categories table...")
        
        risk_test_query = f"""
        SELECT 
            balance_range,
            min_balance,
            max_balance,
            risk_score,
            risk_description
        FROM `{project_id}.{dataset_id}.risk_categories`
        ORDER BY min_balance
        """
        
        job = client.query(risk_test_query)
        results = job.result()
        
        print("Risk Categories Data:")
        for row in results:
            print(f"  {row.balance_range}: ${row.min_balance:,} - ${row.max_balance:,} (Risk Score: {row.risk_score}) - {row.risk_description}")
        
        # 5. Test a sample risk score scenario
        print("\n🧪 Testing Risk Score VLOOKUP scenario...")
        
        vlookup_risk_query = f"""
        SELECT 
            c.customer_id,
            c.balance,
            CASE 
                WHEN c.balance <= 10000 THEN 'LOW'
                WHEN c.balance <= 50000 THEN 'MEDIUM'
                WHEN c.balance <= 100000 THEN 'HIGH'
                ELSE 'PREMIUM'
            END as balance_category,
            r.risk_score,
            r.risk_description
        FROM `{project_id}.{dataset_id}.customers` c
        LEFT JOIN `{project_id}.{dataset_id}.risk_categories` r
            ON (CASE 
                WHEN c.balance <= 10000 THEN 'LOW'
                WHEN c.balance <= 50000 THEN 'MEDIUM'
                WHEN c.balance <= 100000 THEN 'HIGH'
                ELSE 'PREMIUM'
            END) = r.balance_range
        WHERE c.balance > 0
        ORDER BY c.balance DESC
        LIMIT 10
        """
        
        job = client.query(vlookup_risk_query)
        results = job.result()
        
        print("Risk Score VLOOKUP Results:")
        for row in results:
            print(f"  Customer {row.customer_id}: Balance ${row.balance:,.2f} → {row.balance_category} (Risk Score: {row.risk_score}) - {row.risk_description}")
        
        print("\n✅ All missing reference tables created successfully!")
        print("🎯 The enhanced scenarios should now work correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating missing reference tables: {str(e)}")
        return False

if __name__ == "__main__":
    create_missing_reference_tables()
