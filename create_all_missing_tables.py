#!/usr/bin/env python3
"""
Create All Missing Reference Tables
Create all reference tables needed for all enhanced scenarios.
"""

import pandas as pd
from google.cloud import bigquery
import logging

def create_all_missing_reference_tables():
    """Create all missing reference tables for enhanced scenarios."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print("🔄 Creating all missing reference tables...")
        
        # 1. Customer Activity Reference Table
        customer_activity_data = []
        for i in range(1, 101):  # Create 100 sample customers
            customer_activity_data.append({
                'customer_id': f'CUST_{i:06d}',
                'transaction_count': max(0, 15 - (i % 20)),  # Varied transaction counts
                'activity_score': min(10, i % 12)
            })
        
        customer_activity_df = pd.DataFrame(customer_activity_data)
        
        # Create table in BigQuery
        table_id = f"{project_id}.{dataset_id}.customer_activity"
        schema = [
            bigquery.SchemaField("customer_id", "STRING"),
            bigquery.SchemaField("transaction_count", "INT64"),
            bigquery.SchemaField("activity_score", "INT64"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        job = client.load_table_from_dataframe(customer_activity_df, table)
        job.result()
        print(f"✅ Created customer_activity table with {len(customer_activity_data)} rows")
        
        # 2. Credit Limits Reference Table
        credit_limits_data = [
            {'account_type': 'SAVINGS', 'income_tier': 'LOW_INCOME', 'max_credit_limit': 5000},
            {'account_type': 'SAVINGS', 'income_tier': 'MID_INCOME', 'max_credit_limit': 15000},
            {'account_type': 'SAVINGS', 'income_tier': 'HIGH_INCOME', 'max_credit_limit': 50000},
            {'account_type': 'CHECKING', 'income_tier': 'LOW_INCOME', 'max_credit_limit': 2000},
            {'account_type': 'CHECKING', 'income_tier': 'MID_INCOME', 'max_credit_limit': 8000},
            {'account_type': 'CHECKING', 'income_tier': 'HIGH_INCOME', 'max_credit_limit': 25000},
            {'account_type': 'PREMIUM', 'income_tier': 'LOW_INCOME', 'max_credit_limit': 10000},
            {'account_type': 'PREMIUM', 'income_tier': 'MID_INCOME', 'max_credit_limit': 50000},
            {'account_type': 'PREMIUM', 'income_tier': 'HIGH_INCOME', 'max_credit_limit': 200000},
            {'account_type': 'BUSINESS', 'income_tier': 'LOW_INCOME', 'max_credit_limit': 25000},
            {'account_type': 'BUSINESS', 'income_tier': 'MID_INCOME', 'max_credit_limit': 100000},
            {'account_type': 'BUSINESS', 'income_tier': 'HIGH_INCOME', 'max_credit_limit': 500000}
        ]
        
        credit_limits_df = pd.DataFrame(credit_limits_data)
        
        table_id = f"{project_id}.{dataset_id}.credit_limits"
        schema = [
            bigquery.SchemaField("account_type", "STRING"),
            bigquery.SchemaField("income_tier", "STRING"),
            bigquery.SchemaField("max_credit_limit", "INT64"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        job = client.load_table_from_dataframe(credit_limits_df, table)
        job.result()
        print(f"✅ Created credit_limits table with {len(credit_limits_data)} rows")
        
        # 3. Compliance Rules Reference Table
        compliance_rules_data = [
            {'rule_id': 'KYC_001', 'rule_type': 'KYC', 'balance_threshold': 10000, 'required_docs': 'ID_PROOF', 'compliance_level': 'BASIC'},
            {'rule_id': 'KYC_002', 'rule_type': 'KYC', 'balance_threshold': 50000, 'required_docs': 'ID_PROOF,ADDRESS_PROOF', 'compliance_level': 'ENHANCED'},
            {'rule_id': 'KYC_003', 'rule_type': 'KYC', 'balance_threshold': 100000, 'required_docs': 'ID_PROOF,ADDRESS_PROOF,INCOME_PROOF', 'compliance_level': 'PREMIUM'},
            {'rule_id': 'AML_001', 'rule_type': 'AML', 'balance_threshold': 25000, 'required_docs': 'TRANSACTION_HISTORY', 'compliance_level': 'STANDARD'},
            {'rule_id': 'AML_002', 'rule_type': 'AML', 'balance_threshold': 75000, 'required_docs': 'TRANSACTION_HISTORY,SOURCE_OF_FUNDS', 'compliance_level': 'ENHANCED'},
            {'rule_id': 'PEP_001', 'rule_type': 'PEP', 'balance_threshold': 0, 'required_docs': 'PEP_DECLARATION', 'compliance_level': 'MANDATORY'}
        ]
        
        compliance_rules_df = pd.DataFrame(compliance_rules_data)
        
        table_id = f"{project_id}.{dataset_id}.compliance_rules"
        schema = [
            bigquery.SchemaField("rule_id", "STRING"),
            bigquery.SchemaField("rule_type", "STRING"),
            bigquery.SchemaField("balance_threshold", "INT64"),
            bigquery.SchemaField("required_docs", "STRING"),
            bigquery.SchemaField("compliance_level", "STRING"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        job = client.load_table_from_dataframe(compliance_rules_df, table)
        job.result()
        print(f"✅ Created compliance_rules table with {len(compliance_rules_data)} rows")
        
        # 4. Product Matrix Reference Table
        product_matrix_data = [
            {'product_code': 'SAV_BASIC', 'account_type': 'SAVINGS', 'customer_tier': 'BRONZE', 'eligibility_score': 1, 'min_balance': 100},
            {'product_code': 'SAV_PREMIUM', 'account_type': 'SAVINGS', 'customer_tier': 'GOLD', 'eligibility_score': 5, 'min_balance': 10000},
            {'product_code': 'CHK_BASIC', 'account_type': 'CHECKING', 'customer_tier': 'BRONZE', 'eligibility_score': 1, 'min_balance': 25},
            {'product_code': 'CHK_PREMIUM', 'account_type': 'CHECKING', 'customer_tier': 'SILVER', 'eligibility_score': 3, 'min_balance': 1000},
            {'product_code': 'INV_BASIC', 'account_type': 'INVESTMENT', 'customer_tier': 'SILVER', 'eligibility_score': 4, 'min_balance': 5000},
            {'product_code': 'INV_PREMIUM', 'account_type': 'INVESTMENT', 'customer_tier': 'PLATINUM', 'eligibility_score': 8, 'min_balance': 100000},
            {'product_code': 'BUS_BASIC', 'account_type': 'BUSINESS', 'customer_tier': 'BRONZE', 'eligibility_score': 2, 'min_balance': 1000},
            {'product_code': 'BUS_PREMIUM', 'account_type': 'BUSINESS', 'customer_tier': 'GOLD', 'eligibility_score': 6, 'min_balance': 25000}
        ]
        
        product_matrix_df = pd.DataFrame(product_matrix_data)
        
        table_id = f"{project_id}.{dataset_id}.product_matrix"
        schema = [
            bigquery.SchemaField("product_code", "STRING"),
            bigquery.SchemaField("account_type", "STRING"),
            bigquery.SchemaField("customer_tier", "STRING"),
            bigquery.SchemaField("eligibility_score", "INT64"),
            bigquery.SchemaField("min_balance", "INT64"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table, exists_ok=True)
        job = client.load_table_from_dataframe(product_matrix_df, table)
        job.result()
        print(f"✅ Created product_matrix table with {len(product_matrix_data)} rows")
        
        # 5. Test one of the complex scenarios
        print("\n🧪 Testing Account Status Complex Logic scenario...")
        
        test_query = f"""
        WITH customer_with_activity AS (
            SELECT 
                c.customer_id,
                c.balance,
                COALESCE(ca.transaction_count, 0) as transaction_count,
                CASE 
                    WHEN c.balance > 0 AND COALESCE(ca.transaction_count, 0) > 5 THEN 'ACTIVE'
                    WHEN c.balance > 0 THEN 'DORMANT'
                    ELSE 'INACTIVE'
                END as account_status
            FROM `{project_id}.{dataset_id}.customers` c
            LEFT JOIN `{project_id}.{dataset_id}.customer_activity` ca
                ON c.customer_id = ca.customer_id
            WHERE c.balance > 0
        )
        SELECT 
            customer_id,
            balance,
            transaction_count,
            account_status
        FROM customer_with_activity
        ORDER BY balance DESC
        LIMIT 10
        """
        
        job = client.query(test_query)
        results = job.result()
        
        print("Account Status Results:")
        for row in results:
            print(f"  Customer {row.customer_id}: Balance ${row.balance:,.2f}, Transactions: {row.transaction_count} → {row.account_status}")
        
        print("\n✅ All missing reference tables created successfully!")
        print("🎯 All enhanced scenarios should now work correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating missing reference tables: {str(e)}")
        return False

if __name__ == "__main__":
    create_all_missing_reference_tables()
