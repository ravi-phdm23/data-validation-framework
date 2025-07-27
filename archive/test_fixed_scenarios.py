#!/usr/bin/env python3
"""
Test Fixed Column Reference Scenarios
Test the corrected compliance and product eligibility scenarios.
"""

from google.cloud import bigquery

def test_fixed_scenarios():
    """Test the fixed compliance and product eligibility scenarios."""
    
    try:
        # Initialize BigQuery client
        project_id = "cohesive-apogee-411113"
        dataset_id = "banking_sample_data"
        client = bigquery.Client(project=project_id)
        
        print("🧪 Testing fixed compliance scenario...")
        
        # Test the corrected compliance scenario
        compliance_query = f"""
        WITH source_with_rules AS (
            SELECT 
                s.customer_id,
                s.balance,
                CASE 
                    WHEN s.balance >= 100000 THEN 'KYC_003'
                    WHEN s.balance >= 50000 THEN 'KYC_002'
                    ELSE 'KYC_001'
                END as rule_category
            FROM `{project_id}.{dataset_id}.customers` s
            WHERE s.balance > 0
        ),
        source_with_lookup AS (
            SELECT 
                sr.*,
                r.compliance_level,
                r.required_docs,
                CASE 
                    WHEN r.rule_id IS NOT NULL THEN 'FOUND'
                    ELSE 'NOT_FOUND'
                END as lookup_status
            FROM source_with_rules sr
            LEFT JOIN `{project_id}.{dataset_id}.compliance_rules` r 
                ON sr.rule_category = r.rule_id
        )
        SELECT 
            customer_id,
            balance,
            rule_category,
            compliance_level,
            required_docs,
            lookup_status
        FROM source_with_lookup
        ORDER BY balance DESC
        LIMIT 10
        """
        
        job = client.query(compliance_query)
        results = job.result()
        
        print("✅ Fixed Compliance Results:")
        compliance_found = 0
        compliance_total = 0
        
        for row in results:
            compliance_total += 1
            if row.lookup_status == 'FOUND':
                compliance_found += 1
            print(f"  Customer {row.customer_id}: ${row.balance:,.2f} → {row.rule_category} ({row.compliance_level}) [{row.lookup_status}]")
        
        compliance_rate = (compliance_found / compliance_total * 100) if compliance_total > 0 else 0
        print(f"📊 Compliance Lookup Success: {compliance_found}/{compliance_total} ({compliance_rate:.1f}%)")
        
        print("\n🧪 Testing fixed product eligibility scenario...")
        
        # Test the corrected product eligibility scenario  
        product_query = f"""
        WITH source_with_tiers AS (
            SELECT 
                s.customer_id,
                s.balance,
                s.account_type,
                CASE 
                    WHEN s.balance > 100000 THEN 'PLATINUM'
                    WHEN s.balance > 75000 THEN 'GOLD'
                    WHEN s.balance > 25000 THEN 'SILVER'
                    ELSE 'BRONZE'
                END as customer_tier
            FROM `{project_id}.{dataset_id}.customers` s
            WHERE s.balance > 0 AND s.account_type IN ('SAVINGS', 'CHECKING', 'BUSINESS', 'INVESTMENT')
        ),
        source_with_lookup AS (
            SELECT 
                st.*,
                r.product_code,
                r.eligibility_score,
                r.min_balance,
                CASE 
                    WHEN r.product_code IS NOT NULL THEN 'FOUND'
                    ELSE 'NOT_FOUND'
                END as lookup_status
            FROM source_with_tiers st
            LEFT JOIN `{project_id}.{dataset_id}.product_matrix` r 
                ON CAST(st.account_type AS STRING) = CAST(r.account_type AS STRING)
                AND CAST(st.customer_tier AS STRING) = CAST(r.customer_tier AS STRING)
        )
        SELECT 
            customer_id,
            balance,
            account_type,
            customer_tier,
            product_code,
            eligibility_score,
            lookup_status
        FROM source_with_lookup
        ORDER BY balance DESC
        LIMIT 10
        """
        
        job = client.query(product_query)
        results = job.result()
        
        print("✅ Fixed Product Eligibility Results:")
        product_found = 0
        product_total = 0
        
        for row in results:
            product_total += 1
            if row.lookup_status == 'FOUND':
                product_found += 1
            print(f"  Customer {row.customer_id}: {row.account_type} + {row.customer_tier} → {row.product_code} (Score: {row.eligibility_score}) [{row.lookup_status}]")
        
        product_rate = (product_found / product_total * 100) if product_total > 0 else 0
        print(f"📊 Product Lookup Success: {product_found}/{product_total} ({product_rate:.1f}%)")
        
        overall_success = compliance_rate > 80 and product_rate > 80
        
        if overall_success:
            print("\n✅ Both scenarios are working correctly!")
            return True
        else:
            print("\n❌ Some scenarios still have issues")
            return False
        
    except Exception as e:
        print(f"❌ Error testing fixed scenarios: {str(e)}")
        return False

if __name__ == "__main__":
    test_fixed_scenarios()
