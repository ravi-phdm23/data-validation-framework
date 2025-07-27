"""
Create composite key test tables (DDL only) in BigQuery
This script creates empty tables with composite primary key structures
"""

from google.cloud import bigquery
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_composite_key_table_structures():
    """Create table structures for composite key testing"""
    
    project_id = "cohesive-apogee-411113"
    dataset_id = "banking_sample_data"
    
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Table creation queries (DDL only - no INSERT statements)
    tables = {
        'account_type_summary': '''
        CREATE OR REPLACE TABLE `cohesive-apogee-411113.banking_sample_data.account_type_summary` (
            customer_id STRING,
            account_type STRING,
            total_balance FLOAT64,
            account_count INT64,
            created_date DATE
        )
        ''',
        
        'regional_analysis': '''
        CREATE OR REPLACE TABLE `cohesive-apogee-411113.banking_sample_data.regional_analysis` (
            region STRING,
            product_type STRING,
            quarter STRING,
            total_revenue FLOAT64,
            customer_count INT64,
            avg_transaction_value FLOAT64
        )
        ''',
        
        'account_summary_target': '''
        CREATE OR REPLACE TABLE `cohesive-apogee-411113.banking_sample_data.account_summary_target` (
            cust_id STRING,
            acct_type STRING,
            balance_total FLOAT64,
            num_accounts INT64,
            setup_date DATE
        )
        ''',
        
        'region_product_target': '''
        CREATE OR REPLACE TABLE `cohesive-apogee-411113.banking_sample_data.region_product_target` (
            area STRING,
            product_line STRING,
            time_period STRING,
            revenue_total FLOAT64,
            cust_count INT64,
            avg_txn_value FLOAT64
        )
        '''
    }
    
    # Create each table
    for table_name, query in tables.items():
        try:
            logging.info(f"Creating table structure: {table_name}")
            
            # Execute the query
            job = client.query(query)
            job.result()  # Wait for completion
            
            logging.info(f"✅ Successfully created table structure: {table_name}")
            
        except Exception as e:
            logging.error(f"❌ Failed to create table {table_name}: {str(e)}")
    
    logging.info("🎉 Composite key table structures created!")
    logging.info("📝 Note: Tables are empty. You can use existing test data or manual INSERT statements in BigQuery console.")

if __name__ == "__main__":
    create_composite_key_table_structures()
