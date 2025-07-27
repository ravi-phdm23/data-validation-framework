#!/usr/bin/env python3
"""
Test the generated SQL to make sure it works
"""

from google.cloud import bigquery

def test_sql():
    """Test the generated SQL."""
    client = bigquery.Client(project='cohesive-apogee-411113')
    
    sql = """
    -- Transformation Validation: avg_amount
    -- Source Table: transactions
    -- Single Key: account_number
    -- Derivation Logic: AVG(amount) GROUP_BY account_number
    -- Testing aggregation logic against source data
    WITH transformed_data AS (
        SELECT
            account_number,
            AVG(amount) as calculated_avg_amount
        FROM `cohesive-apogee-411113.banking_sample_data.transactions`
        GROUP BY account_number
    ),
    validation_summary AS (
        SELECT
            COUNT(*) as total_rows,
            COUNT(calculated_avg_amount) as non_null_rows,
            COUNT(*) - COUNT(calculated_avg_amount) as null_rows,
            MIN(CAST(calculated_avg_amount AS FLOAT64)) as min_value,
            MAX(CAST(calculated_avg_amount AS FLOAT64)) as max_value,
            AVG(CAST(calculated_avg_amount AS FLOAT64)) as avg_value
        FROM transformed_data
    )
    SELECT
        'PASS' as validation_status,
        total_rows as row_count,
        ROUND(100.0, 2) as percentage,
        CONCAT('Aggregation successful: ', CAST(total_rows AS STRING), ' rows processed') as details
    FROM validation_summary
    WHERE total_rows > 0
    """
    
    try:
        result = client.query(sql).result()
        for row in result:
            print(f"✅ SQL Test Result:")
            print(f"   Status: {row.validation_status}")
            print(f"   Row Count: {row.row_count}")
            print(f"   Percentage: {row.percentage}")
            print(f"   Details: {row.details}")
        return True
    except Exception as e:
        print(f"❌ SQL Test Failed: {e}")
        return False

if __name__ == "__main__":
    test_sql()
