#!/usr/bin/env python3
"""
Test Scenario S001: Customer Full Name Validation
Let's test our first validation scenario together!
"""

from google.cloud import bigquery
import pandas as pd

def test_scenario_s001():
    """Test Customer Full Name Validation scenario."""
    
    print("🧪 Testing Scenario S001: Customer Full Name Validation")
    print("=" * 60)
    print("Source: customers → Target: customer_summary")
    print("Logic: CONCAT(first_name, ' ', last_name)")
    print("Expected: Validate calculated vs existing full names")
    print()
    
    project_id = "cohesive-apogee-411113"
    dataset_id = "banking_sample_data"
    
    try:
        # Initialize BigQuery client
        client = bigquery.Client(project=project_id)
        
        # Let's first examine the data to understand what we're working with
        print("🔍 Step 1: Examining source data (customers table)")
        source_query = f"""
        SELECT 
            customer_id,
            first_name,
            last_name,
            full_name as existing_full_name,
            CONCAT(first_name, ' ', last_name) as calculated_full_name,
            CASE 
                WHEN CONCAT(first_name, ' ', last_name) = full_name THEN 'MATCH'
                ELSE 'MISMATCH'
            END as comparison_result
        FROM `{project_id}.{dataset_id}.customers`
        LIMIT 10
        """
        
        source_results = client.query(source_query).to_dataframe()
        print("Sample source data:")
        print(source_results.to_string(index=False))
        print()
        
        # Now check the target table
        print("🔍 Step 2: Examining target data (customer_summary table)")
        target_query = f"""
        SELECT 
            cust_id,
            calculated_full_name,
            existing_full_name,
            CASE 
                WHEN calculated_full_name = existing_full_name THEN 'MATCH'
                ELSE 'MISMATCH'
            END as target_comparison
        FROM `{project_id}.{dataset_id}.customer_summary`
        LIMIT 10
        """
        
        target_results = client.query(target_query).to_dataframe()
        print("Sample target data:")
        print(target_results.to_string(index=False))
        print()
        
        # Now let's run the actual validation SQL that our framework would generate
        print("🚀 Step 3: Running validation SQL (what our framework generates)")
        
        validation_sql = f"""
        -- REAL Transformation Validation: calculated_full_name
        -- Source Table: customers vs Target Table: customer_summary
        -- Single Key: customer_id
        -- Derivation Logic: CONCAT(first_name, " ", last_name)
        -- Comparing calculated values with actual target values

        WITH source_calculated AS (
            SELECT 
                customer_id,
                CONCAT(first_name, ' ', last_name) as calculated_calculated_full_name
            FROM `{project_id}.{dataset_id}.customers`
        ),
        target_actual AS (
            SELECT 
                cust_id,
                calculated_full_name as actual_calculated_full_name
            FROM `{project_id}.{dataset_id}.customer_summary`
            WHERE calculated_full_name IS NOT NULL
        ),
        comparison AS (
            SELECT 
                s.customer_id as join_key,
                s.calculated_calculated_full_name,
                t.actual_calculated_full_name,
                CASE 
                    WHEN s.calculated_calculated_full_name IS NULL AND t.actual_calculated_full_name IS NULL THEN 'BOTH_NULL'
                    WHEN s.calculated_calculated_full_name IS NULL THEN 'SOURCE_NULL'
                    WHEN t.actual_calculated_full_name IS NULL THEN 'TARGET_NULL'
                    WHEN CAST(s.calculated_calculated_full_name AS STRING) = CAST(t.actual_calculated_full_name AS STRING) THEN 'MATCH'
                    ELSE 'MISMATCH'
                END as validation_result,
                s.calculated_calculated_full_name as source_value,
                t.actual_calculated_full_name as target_value
            FROM source_calculated s
            FULL OUTER JOIN target_actual t ON s.customer_id = t.cust_id
        ),
        validation_summary AS (
            SELECT 
                COUNT(*) as total_rows,
                COUNTIF(validation_result = 'MATCH') as matching_rows,
                COUNTIF(validation_result = 'MISMATCH') as mismatched_rows,
                COUNTIF(validation_result = 'SOURCE_NULL') as source_null_rows,
                COUNTIF(validation_result = 'TARGET_NULL') as target_null_rows,
                COUNTIF(validation_result = 'BOTH_NULL') as both_null_rows
            FROM comparison
        )
        SELECT 
            CASE 
                WHEN matching_rows = total_rows THEN 'PASS'
                ELSE 'FAIL'
            END as validation_status,
            total_rows as row_count,
            ROUND(matching_rows * 100.0 / NULLIF(total_rows, 0), 2) as percentage,
            CONCAT('Matches: ', CAST(matching_rows AS STRING), 
                   ', Mismatches: ', CAST(mismatched_rows AS STRING),
                   ', Source Nulls: ', CAST(source_null_rows AS STRING),
                   ', Target Nulls: ', CAST(target_null_rows AS STRING)) as details
        FROM validation_summary
        WHERE total_rows > 0
        """
        
        validation_results = client.query(validation_sql).to_dataframe()
        print("🎯 Validation Results:")
        print(validation_results.to_string(index=False))
        print()
        
        # Show sample mismatches if any
        if not validation_results.empty and 'FAIL' in validation_results['validation_status'].values:
            print("🔍 Sample Mismatches:")
            mismatch_query = f"""
            WITH source_calculated AS (
                SELECT 
                    customer_id,
                    CONCAT(first_name, ' ', last_name) as calculated_full_name
                FROM `{project_id}.{dataset_id}.customers`
            ),
            target_actual AS (
                SELECT 
                    cust_id,
                    calculated_full_name
                FROM `{project_id}.{dataset_id}.customer_summary`
                WHERE calculated_full_name IS NOT NULL
            )
            SELECT 
                s.customer_id,
                s.calculated_full_name as source_calculation,
                t.calculated_full_name as target_value,
                'MISMATCH' as issue
            FROM source_calculated s
            FULL OUTER JOIN target_actual t ON s.customer_id = t.cust_id
            WHERE s.calculated_full_name != t.calculated_full_name
               OR (s.calculated_full_name IS NULL) != (t.calculated_full_name IS NULL)
            LIMIT 5
            """
            
            mismatch_results = client.query(mismatch_query).to_dataframe()
            print(mismatch_results.to_string(index=False))
        
        print("\n✅ Scenario S001 test completed!")
        print("📊 This scenario demonstrates real source vs target validation")
        print("🔧 Ready to test in the Streamlit app!")
        
    except Exception as e:
        print(f"❌ Error testing scenario: {str(e)}")
        print("💡 Make sure you have BigQuery access to cohesive-apogee-411113")

if __name__ == "__main__":
    test_scenario_s001()
