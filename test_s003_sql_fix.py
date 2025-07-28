#!/usr/bin/env python3
"""
Test S003 SQL generation fix
"""

from sql_generator import create_enhanced_transformation_sql

def test_s003_sql_fix():
    """Test if the S003 SQL generation now works correctly."""
    
    print("🔍 Testing S003 SQL generation fix...")
    print("=" * 60)
    
    # Test with original S003 scenario
    sql_query = create_enhanced_transformation_sql(
        source_table='transactions',
        target_table='transaction_history',  # Using existing table
        source_join_key='transaction_id',
        target_join_key='transaction_id',    # Assuming same key name
        target_column='status_description',
        derivation_logic='CASE WHEN amount > 0 THEN "Credit" ELSE "Debit" END',
        project_id='cohesive-apogee-411113',
        dataset_id='banking_sample_data'
    )
    
    print("Generated SQL:")
    print("=" * 60)
    print(sql_query)
    print("=" * 60)
    
    # Check if the CASE WHEN logic is correctly preserved
    if 'CASE WHEN amount > 0 THEN "Credit" ELSE "Debit" END' in sql_query:
        print("✅ SUCCESS: CASE WHEN logic correctly preserved in SQL!")
    elif 'amount as calculated_status_description' in sql_query:
        print("❌ ISSUE: Still converting to simple column reference")
    elif 'CASE WHEN' in sql_query:
        print("⚠️ PARTIAL: CASE WHEN found but may not be exact match")
    else:
        print("❌ ISSUE: No CASE WHEN logic found in generated SQL")

if __name__ == "__main__":
    test_s003_sql_fix()
