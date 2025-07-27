#!/usr/bin/env python3
"""
Create Test Tables in BigQuery for Source-Target Validation Scenarios
This script creates multiple tables with different join key column names to test
the enhanced validation framework with separate Source_Join_Key and Target_Join_Key.
"""

from google.cloud import bigquery
import os
from datetime import datetime, timedelta
import random

# Configuration
PROJECT_ID = "cohesive-apogee-411113"
DATASET_ID = "banking_sample_data"

def get_bigquery_client():
    """Initialize BigQuery client."""
    try:
        client = bigquery.Client(project=PROJECT_ID)
        return client
    except Exception as e:
        print(f"❌ Error initializing BigQuery client: {e}")
        return None

def create_source_tables(client):
    """Create source tables with original column names."""
    
    print("🔧 Creating source tables...")
    
    # 1. Customer Master Table (Original)
    customers_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.customers_source` AS
    SELECT
        customer_id,
        first_name,
        last_name,
        full_name,
        account_number,
        account_type,
        balance,
        account_open_date,
        address,
        city,
        state,
        risk_score,
        account_status,
        monthly_income
    FROM `{PROJECT_ID}.{DATASET_ID}.customers`
    """
    
    # 2. Transaction Details Table (Original)
    transactions_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.transactions_source` AS
    SELECT
        transaction_id,
        account_number,
        transaction_type,
        amount,
        transaction_date,
        channel,
        merchant,
        transaction_city,
        transaction_state,
        status,
        processing_fee
    FROM `{PROJECT_ID}.{DATASET_ID}.transactions`
    """
    
    try:
        # Create customers_source
        client.query(customers_sql).result()
        print("✅ Created: customers_source")
        
        # Create transactions_source  
        client.query(transactions_sql).result()
        print("✅ Created: transactions_source")
        
    except Exception as e:
        print(f"❌ Error creating source tables: {e}")

def create_target_tables_different_keys(client):
    """Create target tables with different join key column names."""
    
    print("🎯 Creating target tables with different join key names...")
    
    # 1. Customer Summary Table (Different join key: customer_id -> cust_id)
    customer_summary_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.customer_summary` AS
    SELECT
        customer_id as cust_id,  -- Different column name
        CONCAT(first_name, ' ', last_name) as calculated_full_name,
        full_name as existing_full_name,
        balance as account_balance,
        CASE 
            WHEN balance > 50000 THEN 'LOW'
            WHEN balance > 10000 THEN 'MEDIUM'
            ELSE 'HIGH'
        END as risk_level,
        CASE 
            WHEN balance > 0 THEN 'ACTIVE'
            ELSE 'INACTIVE'
        END as calculated_account_status,
        account_status as existing_account_status,
        CASE 
            WHEN risk_score < 300 THEN 'YOUNG'
            WHEN risk_score < 600 THEN 'MIDDLE'
            ELSE 'SENIOR'
        END as age_category,
        account_open_date,
        CURRENT_TIMESTAMP() as summary_created_date
    FROM `{PROJECT_ID}.{DATASET_ID}.customers`
    """
    
    # 2. Account Profiles Table (Different join key: customer_id -> customer_reference)
    account_profiles_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.account_profiles` AS
    SELECT
        customer_id as customer_reference,  -- Different column name
        UPPER(CONCAT(first_name, ' ', last_name)) as customer_name_upper,
        full_name as full_customer_name,
        balance as current_balance,
        account_type as profile_type,
        city as location,
        state as region,
        CASE 
            WHEN balance > 25000 THEN 'PREMIUM'
            WHEN balance > 5000 THEN 'STANDARD'
            ELSE 'BASIC'
        END as tier_level,
        account_open_date as profile_created_date
    FROM `{PROJECT_ID}.{DATASET_ID}.customers`
    """
    
    # 3. Transaction History Table (Different join key: transaction_id -> txn_reference_id)
    transaction_history_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.transaction_history` AS
    SELECT
        transaction_id as txn_reference_id,  -- Different column name
        account_number as account_id,        -- Different column name
        transaction_date as txn_date,
        amount as transaction_amount,
        amount * 1.05 as processed_amount,   -- With processing fee
        transaction_type as txn_type,
        channel as transaction_channel,
        merchant as vendor_name,
        transaction_city as txn_city,
        CASE 
            WHEN amount > 1000 THEN 'HIGH_VALUE'
            WHEN amount > 100 THEN 'MEDIUM_VALUE'
            ELSE 'LOW_VALUE'
        END as value_category,
        CURRENT_TIMESTAMP() as processed_date
    FROM `{PROJECT_ID}.{DATASET_ID}.transactions`
    """
    
    # 4. Monthly Summaries Table (Different join key: account_number -> account_ref)
    monthly_summaries_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.monthly_summaries` AS
    SELECT
        account_number as account_ref,  -- Different column name
        EXTRACT(YEAR FROM transaction_date) as summary_year,
        EXTRACT(MONTH FROM transaction_date) as summary_month,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        MIN(amount) as min_amount,
        MAX(amount) as max_amount,
        MAX(transaction_date) as latest_transaction_date,
        MIN(transaction_date) as earliest_transaction_date
    FROM `{PROJECT_ID}.{DATASET_ID}.transactions`
    GROUP BY 
        account_number,
        EXTRACT(YEAR FROM transaction_date),
        EXTRACT(MONTH FROM transaction_date)
    """
    
    try:
        # Create customer_summary
        client.query(customer_summary_sql).result()
        print("✅ Created: customer_summary (cust_id as join key)")
        
        # Create account_profiles
        client.query(account_profiles_sql).result()
        print("✅ Created: account_profiles (customer_reference as join key)")
        
        # Create transaction_history
        client.query(transaction_history_sql).result()
        print("✅ Created: transaction_history (txn_reference_id as join key)")
        
        # Create monthly_summaries
        client.query(monthly_summaries_sql).result()
        print("✅ Created: monthly_summaries (account_ref as join key)")
        
    except Exception as e:
        print(f"❌ Error creating target tables: {e}")

def create_legacy_tables(client):
    """Create legacy-style tables with abbreviated column names."""
    
    print("🏛️ Creating legacy tables with abbreviated column names...")
    
    # Legacy Customer Data Table
    legacy_customers_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.legacy_cust_data` AS
    SELECT
        customer_id as cust_pk,     -- Primary key with legacy naming
        first_name as fname,
        last_name as lname,
        full_name as full_nm,
        balance as bal,
        account_type as acct_type,
        account_open_date as reg_dt,
        city as loc_city,
        state as loc_state
    FROM `{PROJECT_ID}.{DATASET_ID}.customers`
    """
    
    # Legacy Transaction Data Table
    legacy_transactions_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.legacy_txn_data` AS
    SELECT
        transaction_id as txn_pk,           -- Primary key with legacy naming
        account_number as acct_num,         -- Different column name
        transaction_date as txn_dt,
        amount as txn_amt,
        transaction_type as txn_typ,
        channel as chnl,
        merchant as merch_name
    FROM `{PROJECT_ID}.{DATASET_ID}.transactions`
    """
    
    try:
        # Create legacy_cust_data
        client.query(legacy_customers_sql).result()
        print("✅ Created: legacy_cust_data (cust_pk as join key)")
        
        # Create legacy_txn_data
        client.query(legacy_transactions_sql).result()
        print("✅ Created: legacy_txn_data (txn_pk as join key)")
        
    except Exception as e:
        print(f"❌ Error creating legacy tables: {e}")

def create_cross_system_tables(client):
    """Create tables simulating different system naming conventions."""
    
    print("🔄 Creating cross-system tables with different naming conventions...")
    
    # Modern CRM System Table
    crm_customers_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.crm_customer_profiles` AS
    SELECT
        customer_id as crm_customer_id,     -- CRM system naming
        CONCAT(first_name, ' ', last_name) as full_customer_name,
        full_name as existing_full_name,
        account_number as contact_reference,
        balance as account_value,
        account_open_date as onboarding_date,
        CASE 
            WHEN balance > 100000 THEN 'VIP'
            WHEN balance > 50000 THEN 'GOLD'
            WHEN balance > 10000 THEN 'SILVER'
            ELSE 'BRONZE'
        END as customer_tier
    FROM `{PROJECT_ID}.{DATASET_ID}.customers`
    """
    
    # ERP Financial System Table
    erp_accounts_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.erp_account_balances` AS
    SELECT
        customer_id as erp_account_id,      -- ERP system naming
        balance as current_balance,
        balance * 0.05 as interest_earned,
        balance + (balance * 0.05) as projected_balance,
        account_type as account_classification,
        CASE 
            WHEN balance < 1000 THEN 'MINIMUM'
            WHEN balance < 10000 THEN 'STANDARD'
            ELSE 'PREMIUM'
        END as balance_tier,
        account_open_date as account_opened_date
    FROM `{PROJECT_ID}.{DATASET_ID}.customers`
    """
    
    # Payment Processing System Table
    payment_transactions_sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.payment_processor_data` AS
    SELECT
        transaction_id as payment_id,           -- Payment system naming
        account_number as payer_account,        -- Different naming
        amount as payment_amount,
        amount * 0.03 as processing_fee,        -- Processing fee
        amount + (amount * 0.03) as total_charge,
        transaction_date as payment_date,
        transaction_type as payment_method,
        merchant as payee_name,
        CASE 
            WHEN amount > 5000 THEN 'LARGE'
            WHEN amount > 500 THEN 'MEDIUM'
            ELSE 'SMALL'
        END as payment_size
    FROM `{PROJECT_ID}.{DATASET_ID}.transactions`
    """
    
    try:
        # Create CRM table
        client.query(crm_customers_sql).result()
        print("✅ Created: crm_customer_profiles (crm_customer_id as join key)")
        
        # Create ERP table
        client.query(erp_accounts_sql).result()
        print("✅ Created: erp_account_balances (erp_account_id as join key)")
        
        # Create Payment Processing table
        client.query(payment_transactions_sql).result()
        print("✅ Created: payment_processor_data (payment_id as join key)")
        
    except Exception as e:
        print(f"❌ Error creating cross-system tables: {e}")

def display_table_summary(client):
    """Display summary of all created tables and their join keys."""
    
    print("\n" + "="*80)
    print("📊 TABLE SUMMARY - JOIN KEY MAPPING SCENARIOS")
    print("="*80)
    
    table_mappings = [
        ("Source Tables", [
            ("customers_source", "customer_id", "Original customer master table"),
            ("transactions_source", "transaction_id", "Original transaction table")
        ]),
        ("Target Tables with Different Join Keys", [
            ("customer_summary", "cust_id", "customer_id → cust_id"),
            ("account_profiles", "customer_reference", "customer_id → customer_reference"),
            ("transaction_history", "txn_reference_id", "transaction_id → txn_reference_id"),
            ("monthly_summaries", "account_ref", "account_number → account_ref")
        ]),
        ("Legacy System Tables", [
            ("legacy_cust_data", "cust_pk", "customer_id → cust_pk"),
            ("legacy_txn_data", "txn_pk", "transaction_id → txn_pk")
        ]),
        ("Cross-System Tables", [
            ("crm_customer_profiles", "crm_customer_id", "customer_id → crm_customer_id"),
            ("erp_account_balances", "erp_account_id", "customer_id → erp_account_id"),
            ("payment_processor_data", "payment_id", "transaction_id → payment_id")
        ])
    ]
    
    for category, tables in table_mappings:
        print(f"\n🔹 {category}:")
        for table_name, join_key, description in tables:
            try:
                # Get row count
                count_query = f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.{table_name}`"
                result = client.query(count_query).result()
                row_count = next(result).count
                print(f"   ✅ {table_name:<25} | Join Key: {join_key:<20} | Rows: {row_count:<6} | {description}")
            except Exception as e:
                print(f"   ❌ {table_name:<25} | Error: {str(e)}")

def create_validation_scenarios_excel():
    """Create an Excel file with validation scenarios using the new tables."""
    
    import pandas as pd
    from datetime import datetime
    
    print("\n📋 Creating validation scenarios Excel file...")
    
    # Validation scenarios using different source-target join key combinations
    scenarios = [
        {
            'Scenario_ID': 'DIFF_KEY_001',
            'Scenario_Name': 'Customer Full Name with Different Keys',
            'Description': 'Validate full name transformation with different join keys',
            'Source_Table': 'customers_source',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_id',  # Different!
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
        },
        {
            'Scenario_ID': 'DIFF_KEY_002',
            'Scenario_Name': 'Customer Profile Reference Mapping',
            'Description': 'Validate customer data with reference key mapping',
            'Source_Table': 'customers_source',
            'Target_Table': 'account_profiles',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_reference',  # Different!
            'Target_Column': 'customer_name_upper',
            'Derivation_Logic': 'UPPER(CONCAT(first_name, " ", last_name))',
        },
        {
            'Scenario_ID': 'DIFF_KEY_003',
            'Scenario_Name': 'Transaction History with Processing Fee',
            'Description': 'Validate processed amount with different transaction keys',
            'Source_Table': 'transactions_source',
            'Target_Table': 'transaction_history',
            'Source_Join_Key': 'transaction_id',
            'Target_Join_Key': 'txn_reference_id',  # Different!
            'Target_Column': 'processed_amount',
            'Derivation_Logic': 'amount * 1.05',
        },
        {
            'Scenario_ID': 'DIFF_KEY_004',
            'Scenario_Name': 'Monthly Summary Account Mapping',
            'Description': 'Validate monthly aggregation with account reference',
            'Source_Table': 'transactions_source',
            'Target_Table': 'monthly_summaries',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_ref',  # Different!
            'Target_Column': 'total_amount',
            'Derivation_Logic': 'SUM(amount)',
        },
        {
            'Scenario_ID': 'LEGACY_001',
            'Scenario_Name': 'Legacy Customer Data Validation',
            'Description': 'Validate data against legacy system with abbreviated keys',
            'Source_Table': 'customers_source',
            'Target_Table': 'legacy_cust_data',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_pk',  # Legacy naming!
            'Target_Column': 'fname',
            'Derivation_Logic': 'first_name',
        },
        {
            'Scenario_ID': 'LEGACY_002',
            'Scenario_Name': 'Legacy Transaction Data Validation',
            'Description': 'Validate transaction data against legacy system',
            'Source_Table': 'transactions_source',
            'Target_Table': 'legacy_txn_data',
            'Source_Join_Key': 'transaction_id',
            'Target_Join_Key': 'txn_pk',  # Legacy naming!
            'Target_Column': 'txn_amt',
            'Derivation_Logic': 'amount',
        },
        {
            'Scenario_ID': 'CRM_001',
            'Scenario_Name': 'CRM System Customer Validation',
            'Description': 'Validate customer data in CRM system format',
            'Source_Table': 'customers_source',
            'Target_Table': 'crm_customer_profiles',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'crm_customer_id',  # CRM naming!
            'Target_Column': 'full_customer_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
        },
        {
            'Scenario_ID': 'ERP_001',
            'Scenario_Name': 'ERP Account Balance Validation',
            'Description': 'Validate account balances in ERP system format',
            'Source_Table': 'customers_source',
            'Target_Table': 'erp_account_balances',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'erp_account_id',  # ERP naming!
            'Target_Column': 'current_balance',
            'Derivation_Logic': 'balance',
        },
        {
            'Scenario_ID': 'PAYMENT_001',
            'Scenario_Name': 'Payment Processor Data Validation',
            'Description': 'Validate payment data with processing fees',
            'Source_Table': 'transactions_source',
            'Target_Table': 'payment_processor_data',
            'Source_Join_Key': 'transaction_id',
            'Target_Join_Key': 'payment_id',  # Payment system naming!
            'Target_Column': 'total_charge',
            'Derivation_Logic': 'amount + (amount * 0.03)',
        }
    ]
    
    # Create DataFrame and Excel file
    df_scenarios = pd.DataFrame(scenarios)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'Different_Join_Keys_Validation_Scenarios_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_scenarios.to_excel(writer, sheet_name='Different_Join_Keys', index=False)
        
        # Instructions sheet
        instructions = pd.DataFrame([
            {'Step': 1, 'Description': 'These scenarios test different source-target join key combinations'},
            {'Step': 2, 'Description': 'Source_Join_Key and Target_Join_Key columns have different values'},
            {'Step': 3, 'Description': 'Upload this file in the Excel Scenarios tab of Streamlit app'},
            {'Step': 4, 'Description': 'Execute scenarios to test the enhanced join key functionality'},
            {'Step': 5, 'Description': 'Compare results to verify cross-table validations work correctly'}
        ])
        instructions.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Join key mapping reference
        mappings = pd.DataFrame([
            {'Source_Table': 'customers_source', 'Source_Key': 'customer_id', 'Target_Table': 'customer_summary', 'Target_Key': 'cust_id'},
            {'Source_Table': 'customers_source', 'Source_Key': 'customer_id', 'Target_Table': 'account_profiles', 'Target_Key': 'customer_reference'},
            {'Source_Table': 'transactions_source', 'Source_Key': 'transaction_id', 'Target_Table': 'transaction_history', 'Target_Key': 'txn_reference_id'},
            {'Source_Table': 'transactions_source', 'Source_Key': 'account_number', 'Target_Table': 'monthly_summaries', 'Target_Key': 'account_ref'},
            {'Source_Table': 'customers_source', 'Source_Key': 'customer_id', 'Target_Table': 'legacy_cust_data', 'Target_Key': 'cust_pk'},
            {'Source_Table': 'transactions_source', 'Source_Key': 'transaction_id', 'Target_Table': 'legacy_txn_data', 'Target_Key': 'txn_pk'},
            {'Source_Table': 'customers_source', 'Source_Key': 'customer_id', 'Target_Table': 'crm_customer_profiles', 'Target_Key': 'crm_customer_id'},
            {'Source_Table': 'customers_source', 'Source_Key': 'customer_id', 'Target_Table': 'erp_account_balances', 'Target_Key': 'erp_account_id'},
            {'Source_Table': 'transactions_source', 'Source_Key': 'transaction_id', 'Target_Table': 'payment_processor_data', 'Target_Key': 'payment_id'}
        ])
        mappings.to_excel(writer, sheet_name='Join_Key_Mappings', index=False)
    
    print(f"✅ Created validation scenarios file: {filename}")
    return filename

def main():
    """Main function to create all test tables."""
    
    print("🚀 Creating BigQuery Test Tables for Source-Target Join Key Scenarios")
    print("="*80)
    print(f"📍 Project: {PROJECT_ID}")
    print(f"📍 Dataset: {DATASET_ID}")
    print("="*80)
    
    # Initialize BigQuery client
    client = get_bigquery_client()
    if not client:
        return
    
    try:
        # Create all table categories
        create_source_tables(client)
        create_target_tables_different_keys(client)
        create_legacy_tables(client)
        create_cross_system_tables(client)
        
        # Display summary
        display_table_summary(client)
        
        # Create validation scenarios Excel
        excel_filename = create_validation_scenarios_excel()
        
        print("\n" + "="*80)
        print("🎉 TABLE CREATION COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\n📋 What was created:")
        print("   • 11 test tables with different join key naming conventions")
        print("   • Source tables with original column names")
        print("   • Target tables with different join key names")
        print("   • Legacy system tables with abbreviated names")
        print("   • Cross-system tables with different naming conventions")
        print(f"   • Validation scenarios Excel file: {excel_filename}")
        
        print("\n🧪 Ready for testing:")
        print("   1. Upload the generated Excel file to your Streamlit app")
        print("   2. Test scenarios with different Source_Join_Key and Target_Join_Key")
        print("   3. Verify that cross-table validations work correctly")
        print("   4. Compare results across different naming conventions")
        
        print("\n🎯 Key Benefits Tested:")
        print("   • Handles different column names between source and target")
        print("   • Supports legacy system integration")
        print("   • Enables cross-system data validation")
        print("   • Validates complex transformation scenarios")
        
    except Exception as e:
        print(f"\n❌ Error in main execution: {e}")

if __name__ == "__main__":
    main()
