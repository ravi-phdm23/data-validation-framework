#!/usr/bin/env python3
"""
Test the exact functions from streamlit_app.py to reproduce the error
"""

import sys
import pandas as pd
from google.cloud import bigquery

# Import the exact functions from streamlit_app.py
def convert_business_logic_to_safe_sql(derivation_logic, source_table, project_id, dataset_id):
    """Convert business logic to safe SQL that works with actual table columns."""
    
    # Known column mappings for our banking tables (based on actual schema)
    customers_columns = ['customer_id', 'first_name', 'last_name', 'full_name', 'account_number', 'account_type', 'balance', 'account_open_date', 'address', 'city', 'state', 'zip_code', 'risk_score', 'account_status', 'monthly_income']
    transactions_columns = ['transaction_id', 'account_number', 'transaction_type', 'amount', 'transaction_date', 'channel', 'merchant', 'transaction_city', 'transaction_state', 'status', 'is_fraudulent', 'processing_fee']
    
    # Determine available columns based on source table
    if source_table.lower() == 'customers':
        available_columns = customers_columns
    elif source_table.lower() == 'transactions':
        available_columns = transactions_columns
    else:
        # Default fallback - use generic approach
        available_columns = ['*']
    
    # Clean and normalize the derivation logic
    logic = derivation_logic.strip()
    
    try:
        # Handle different business logic patterns
        
        # Basic aggregations
        if logic.upper().startswith('SUM(') and 'GROUP_BY' in logic.upper():
            parts = logic.upper().split('GROUP_BY')
            agg_part = parts[0].strip()
            group_part = parts[1].strip()
            
            # Extract column from SUM()
            sum_column = agg_part.replace('SUM(', '').replace(')', '').strip().lower()
            
            # Validate and map columns
            if sum_column == 'balance' and 'balance' in available_columns:
                return f"SUM(balance)"
            elif sum_column == 'amount' and 'amount' in available_columns:
                return f"SUM(amount)"
            else:
                # Fallback to COUNT if column not found
                return f"COUNT(*)"
        
        elif logic.upper().startswith('COUNT(') and 'GROUP_BY' in logic.upper():
            return "COUNT(*)"
        
        elif logic.upper().startswith('AVG(') and 'GROUP_BY' in logic.upper():
            if 'amount' in available_columns:
                return "AVG(amount)"
            elif 'balance' in available_columns:
                return "AVG(balance)"
            else:
                return "COUNT(*)"
        
        # Default fallback for unrecognized logic
        else:
            # If it contains a valid column name, use it
            for col in available_columns:
                if col.lower() in logic.lower():
                    return col
            
            # Ultimate fallback - simple count
            return "1"  # This will work as a basic validation
    
    except Exception as e:
        # Safe fallback for any parsing errors
        return "1"

def create_transformation_validation_sql(source_table, target_table, source_join_key, target_join_key, target_column, derivation_logic, project_id, dataset_id):
    """Create SQL for transformation validation that works with existing tables only.
    Supports both single and composite join keys (comma-separated).
    """
    
    source_ref = f"`{project_id}.{dataset_id}.{source_table}`"
    
    # Handle composite keys - split by comma and clean whitespace
    source_keys = [key.strip() for key in source_join_key.split(',')]
    target_keys = [key.strip() for key in target_join_key.split(',')]
    
    # Create join key selections for SQL
    source_key_select = ', '.join(source_keys)
    source_key_group = ', '.join(source_keys)
    
    # Create a unique identifier for composite keys
    if len(source_keys) > 1:
        composite_key_comment = f"Composite Key: {' + '.join(source_keys)}"
    else:
        composite_key_comment = f"Single Key: {source_keys[0]}"
    
    # Convert business logic to safe SQL
    safe_derivation_logic = convert_business_logic_to_safe_sql(derivation_logic, source_table, project_id, dataset_id)
    
    if any(func in derivation_logic.upper() for func in ['SUM(', 'COUNT(', 'AVG(', 'MAX(', 'MIN(']):
        # Aggregation scenario - test the aggregation logic
        sql = f"""
-- Transformation Validation: {target_column}
-- Source Table: {source_table}
-- {composite_key_comment}
-- Derivation Logic: {derivation_logic}
-- Testing aggregation logic against source data

WITH transformed_data AS (
    SELECT 
        {source_key_select},
        {safe_derivation_logic} as calculated_{target_column}
    FROM {source_ref}
    GROUP BY {source_key_group}
),
validation_summary AS (
    SELECT 
        COUNT(*) as total_rows,
        COUNT(calculated_{target_column}) as non_null_rows,
        COUNT(*) - COUNT(calculated_{target_column}) as null_rows,
        MIN(CAST(calculated_{target_column} AS FLOAT64)) as min_value,
        MAX(CAST(calculated_{target_column} AS FLOAT64)) as max_value,
        AVG(CAST(calculated_{target_column} AS FLOAT64)) as avg_value
    FROM transformed_data
)
SELECT 
    'PASS' as validation_status,
    total_rows as row_count,
    ROUND(100.0, 2) as percentage,
    CONCAT('Aggregation successful: ', CAST(total_rows AS STRING), ' rows processed') as details
FROM validation_summary
WHERE total_rows > 0

UNION ALL

SELECT 
    'INFO' as validation_status,
    non_null_rows as row_count,
    ROUND(non_null_rows * 100.0 / total_rows, 2) as percentage,
    CONCAT('Non-null values: ', CAST(non_null_rows AS STRING), ' out of ', CAST(total_rows AS STRING)) as details
FROM validation_summary
WHERE total_rows > 0
"""
    else:
        # Simple transformation scenario - test the transformation logic
        sql = f"""
-- Transformation Validation: {target_column}
-- Source Table: {source_table}
-- {composite_key_comment}
-- Derivation Logic: {derivation_logic}
-- Testing transformation logic against ALL source data

WITH transformed_data AS (
    SELECT 
        {source_key_select},
        {safe_derivation_logic} as calculated_{target_column}
    FROM {source_ref}
),
validation_summary AS (
    SELECT 
        COUNT(*) as total_rows,
        COUNT(calculated_{target_column}) as non_null_rows,
        COUNT(*) - COUNT(calculated_{target_column}) as null_rows,
        -- Add statistical summary for better validation insights
        MIN(CAST(calculated_{target_column} AS FLOAT64)) as min_value,
        MAX(CAST(calculated_{target_column} AS FLOAT64)) as max_value,
        AVG(CAST(calculated_{target_column} AS FLOAT64)) as avg_value
    FROM transformed_data
)
SELECT 
    'PASS' as validation_status,
    total_rows as row_count,
    ROUND(100.0, 2) as percentage,
    CONCAT('Transformation successful: ', CAST(total_rows AS STRING), ' rows processed') as details
FROM validation_summary

UNION ALL

-- Add additional validation summary
SELECT 
    'INFO' as validation_status,
    non_null_rows as row_count,
    ROUND(non_null_rows * 100.0 / NULLIF(total_rows, 0), 2) as percentage,
    CONCAT('Non-null values: ', CAST(non_null_rows AS STRING), ' out of ', CAST(total_rows AS STRING)) as details
FROM validation_summary
WHERE total_rows > 0
"""
    
    return sql

def test_failing_scenario():
    """Test the failing scenario using exact streamlit_app.py functions."""
    print("🔍 Testing Average_Transaction_Amount scenario with streamlit_app.py functions")
    print("=" * 80)
    
    # The failing scenario details
    scenario_name = 'Average_Transaction_Amount'
    source_table = 'transactions'
    target_table = 'transaction_averages'
    source_join_key = 'account_number'
    target_join_key = 'account_num'
    target_column = 'avg_amount'
    derivation_logic = 'AVG(amount) GROUP_BY account_number'
    project_id = 'cohesive-apogee-411113'
    dataset_id = 'banking_sample_data'
    
    print(f"Scenario: {scenario_name}")
    print(f"Source Table: {source_table}")
    print(f"Derivation Logic: {derivation_logic}")
    print()
    
    # Step 1: Test convert_business_logic_to_safe_sql
    safe_logic = convert_business_logic_to_safe_sql(derivation_logic, source_table, project_id, dataset_id)
    print(f"✅ convert_business_logic_to_safe_sql result: {safe_logic}")
    
    # Step 2: Test create_transformation_validation_sql
    sql = create_transformation_validation_sql(
        source_table, target_table, source_join_key, target_join_key, 
        target_column, derivation_logic, project_id, dataset_id
    )
    
    print(f"\n✅ Generated SQL:")
    print("-" * 40)
    print(sql)
    print("-" * 40)
    
    # Step 3: Try to execute the SQL
    try:
        client = bigquery.Client(project=project_id)
        result = client.query(sql).result()
        
        print(f"\n✅ SQL Execution Results:")
        for row in result:
            print(f"   Status: {row.validation_status}")
            print(f"   Row Count: {row.row_count}")
            print(f"   Percentage: {row.percentage}")
            print(f"   Details: {row.details}")
            print()
        
        return True
    except Exception as e:
        print(f"\n❌ SQL Execution Failed: {e}")
        return False

if __name__ == "__main__":
    test_failing_scenario()
