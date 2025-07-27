#!/usr/bin/env python3
"""
Test Fixed Risk Score Scenario
Test the corrected risk score scenario with proper range-based lookup.
"""

from google.cloud import bigquery

def test_fixed_risk_scenario():
    """Test the fixed risk score scenario."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print("🧪 Testing fixed Risk Score scenario...")
        
        # Test the corrected range-based lookup
        test_query = f"""
        WITH source_with_categories AS (
            SELECT 
                s.customer_id,
                s.balance,
                CASE 
                    WHEN s.balance <= 10000 THEN 'LOW'
                    WHEN s.balance <= 50000 THEN 'MEDIUM'
                    WHEN s.balance <= 100000 THEN 'HIGH'
                    ELSE 'PREMIUM'
                END as balance_category
            FROM `{project_id}.{dataset_id}.customers` s
            WHERE s.balance > 0
        ),
        source_with_lookup AS (
            SELECT 
                sc.*,
                r.risk_score,
                r.risk_description,
                CASE 
                    WHEN r.balance_range IS NOT NULL THEN 'FOUND'
                    ELSE 'NOT_FOUND'
                END as lookup_status
            FROM source_with_categories sc
            LEFT JOIN `{project_id}.{dataset_id}.risk_categories` r 
                ON sc.balance_category = r.balance_range
        )
        SELECT 
            customer_id,
            balance,
            balance_category,
            risk_score,
            risk_description,
            lookup_status
        FROM source_with_lookup
        ORDER BY balance DESC
        LIMIT 10
        """
        
        job = client.query(test_query)
        results = job.result()
        
        print("✅ Fixed Risk Score Results:")
        found_count = 0
        total_count = 0
        
        for row in results:
            total_count += 1
            if row.lookup_status == 'FOUND':
                found_count += 1
            print(f"  Customer {row.customer_id}: ${row.balance:,.2f} → {row.balance_category} (Risk Score: {row.risk_score}) [{row.lookup_status}]")
        
        success_rate = (found_count / total_count * 100) if total_count > 0 else 0
        print(f"\n📊 Lookup Success Rate: {found_count}/{total_count} ({success_rate:.1f}%)")
        
        if success_rate > 90:
            print("✅ Risk Score scenario is working correctly!")
            return True
        else:
            print("❌ Risk Score scenario still has issues")
            return False
        
    except Exception as e:
        print(f"❌ Error testing fixed risk scenario: {str(e)}")
        return False

if __name__ == "__main__":
    test_fixed_risk_scenario()
