#!/usr/bin/env python3
"""
Test the updated transformation validation with SQL query tracking
"""

import pandas as pd
from datetime import datetime

def test_sql_tracking():
    """Test that SQL queries are properly tracked in validation results."""
    
    # Sample validation results with SQL tracking
    sample_results = [
        {
            'Scenario_Name': 'Customer Full Name Test',
            'Source_Table': 'customers',
            'Target_Table': 'customers',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
            'Validation_Status': 'PASS',
            'Row_Count': 1000,
            'Percentage': 100.0,
            'Details': 'Transformation successful: 1000 rows processed',
            'SQL_Query_Used': '''-- Transformation Validation: full_name
-- Source Table: customers
-- Derivation Logic: CONCAT(first_name, " ", last_name)
-- Testing transformation logic against source data

WITH transformed_data AS (
    SELECT 
        customer_id,
        CONCAT(first_name, " ", last_name) as calculated_full_name
    FROM `cohesive-apogee-411113.banking_sample_data.customers`
    LIMIT 1000
),
validation_summary AS (
    SELECT 
        COUNT(*) as total_rows,
        COUNT(calculated_full_name) as non_null_rows,
        COUNT(*) - COUNT(calculated_full_name) as null_rows
    FROM transformed_data
)
SELECT 
    'PASS' as validation_status,
    total_rows as row_count,
    ROUND(100.0, 2) as percentage,
    CONCAT('Transformation successful: ', CAST(total_rows AS STRING), ' rows processed') as details
FROM validation_summary
WHERE total_rows > 0''',
            'Execution_Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'Scenario_Name': 'Transaction Amount Sum Test',
            'Source_Table': 'transactions',
            'Target_Table': 'transactions',
            'Target_Column': 'total_amount',
            'Derivation_Logic': 'SUM(amount)',
            'Validation_Status': 'PASS',
            'Row_Count': 250,
            'Percentage': 100.0,
            'Details': 'Aggregation successful: 250 rows processed',
            'SQL_Query_Used': '''-- Transformation Validation: total_amount
-- Source Table: transactions
-- Derivation Logic: SUM(amount)
-- Testing aggregation logic against source data

WITH transformed_data AS (
    SELECT 
        account_number,
        SUM(amount) as calculated_total_amount
    FROM `cohesive-apogee-411113.banking_sample_data.transactions`
    GROUP BY account_number
),
validation_summary AS (
    SELECT 
        COUNT(*) as total_rows,
        COUNT(calculated_total_amount) as non_null_rows,
        COUNT(*) - COUNT(calculated_total_amount) as null_rows,
        MIN(calculated_total_amount) as min_value,
        MAX(calculated_total_amount) as max_value,
        AVG(CAST(calculated_total_amount AS FLOAT64)) as avg_value
    FROM transformed_data
)
SELECT 
    'PASS' as validation_status,
    total_rows as row_count,
    ROUND(100.0, 2) as percentage,
    CONCAT('Aggregation successful: ', CAST(total_rows AS STRING), ' rows processed') as details
FROM validation_summary
WHERE total_rows > 0''',
            'Execution_Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    # Create DataFrame to demonstrate the structure
    results_df = pd.DataFrame(sample_results)
    
    # Create test Excel file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'test_validation_results_with_sql_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main results with SQL queries
        results_df.to_excel(writer, sheet_name='Validation_Results_With_SQL', index=False)
        
        # SQL queries only
        sql_only = results_df[['Scenario_Name', 'SQL_Query_Used']].drop_duplicates()
        sql_only.to_excel(writer, sheet_name='SQL_Queries_Used', index=False)
        
        # Summary
        summary_data = {
            'Total_Scenarios': len(sample_results),
            'All_Passed': all(r['Validation_Status'] == 'PASS' for r in sample_results),
            'Total_Rows_Processed': sum(r['Row_Count'] for r in sample_results),
            'Generated_At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        pd.DataFrame([summary_data]).to_excel(writer, sheet_name='Summary', index=False)
    
    print(f"✅ Test validation results created: {filename}")
    print("📋 This file demonstrates:")
    print("  • SQL_Query_Used column in main results")
    print("  • Separate SQL_Queries_Used sheet")
    print("  • Full SQL queries for each validation scenario")
    print("  • Execution timestamps and details")
    
    # Display column structure
    print("\n📊 Column Structure:")
    for col in results_df.columns:
        print(f"  • {col}")
    
    print(f"\n🎯 Total scenarios with SQL tracking: {len(sample_results)}")
    return filename

if __name__ == "__main__":
    test_sql_tracking()
