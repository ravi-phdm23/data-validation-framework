#!/usr/bin/env python3
"""
Standalone BigQuery client for testing without Streamlit dependencies
"""

from google.cloud import bigquery
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_query_direct(query, query_name="test_query"):
    """Execute BigQuery query directly without Streamlit dependencies."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        client = bigquery.Client(project=project_id)
        
        logger.info(f"Executing query: {query_name}")
        
        # Execute query
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to DataFrame
        df = results.to_dataframe()
        
        return {
            'success': True,
            'data': df,
            'row_count': len(df),
            'query_name': query_name
        }
        
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'data': None,
            'query_name': query_name
        }

def test_s003_tables():
    """Test S003 table existence and structure."""
    
    print("🔍 Testing S003 tables directly...")
    print("=" * 60)
    
    # Test source table: transactions
    print("Step 1: Testing transactions table...")
    result = execute_query_direct(
        "SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.transactions LIMIT 1",
        "transactions_count"
    )
    
    if result['success']:
        print(f"✅ transactions table exists with {result['data'].iloc[0]['count']} rows")
        
        # Get column info
        columns_result = execute_query_direct(
            "SELECT * FROM cohesive-apogee-411113.banking_sample_data.transactions LIMIT 1",
            "transactions_structure"
        )
        if columns_result['success']:
            print(f"📋 transactions columns: {list(columns_result['data'].columns)}")
    else:
        print(f"❌ transactions table not accessible: {result['error']}")
    
    # Test target table: transaction_summary
    print("\nStep 2: Testing transaction_summary table...")
    result = execute_query_direct(
        "SELECT COUNT(*) as count FROM cohesive-apogee-411113.banking_sample_data.transaction_summary LIMIT 1",
        "transaction_summary_count"
    )
    
    if result['success']:
        print(f"✅ transaction_summary table exists with {result['data'].iloc[0]['count']} rows")
        
        # Get column info
        columns_result = execute_query_direct(
            "SELECT * FROM cohesive-apogee-411113.banking_sample_data.transaction_summary LIMIT 1",
            "transaction_summary_structure"
        )
        if columns_result['success']:
            print(f"📋 transaction_summary columns: {list(columns_result['data'].columns)}")
    else:
        print(f"❌ transaction_summary table not accessible: {result['error']}")
        
        # List available tables to find alternatives
        print("\n🔍 Looking for alternative tables...")
        tables_result = execute_query_direct(
            "SELECT table_name FROM cohesive-apogee-411113.banking_sample_data.INFORMATION_SCHEMA.TABLES WHERE table_name LIKE '%transaction%' OR table_name LIKE '%summary%' ORDER BY table_name",
            "list_transaction_tables"
        )
        
        if tables_result['success']:
            available_tables = tables_result['data']['table_name'].tolist()
            print(f"📋 Available transaction/summary tables:")
            for table in available_tables:
                print(f"  ✅ {table}")
        else:
            print(f"❌ Could not list tables: {tables_result['error']}")

if __name__ == "__main__":
    test_s003_tables()
