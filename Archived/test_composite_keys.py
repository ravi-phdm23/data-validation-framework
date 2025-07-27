"""
Test composite key functionality
This script tests the enhanced parsing and SQL generation functions
"""

def parse_join_keys(join_key_string):
    """Parse comma-separated join keys into a list"""
    if not join_key_string or not join_key_string.strip():
        return []
    
    # Split by comma and clean up whitespace
    keys = [key.strip() for key in join_key_string.split(',')]
    return [key for key in keys if key]  # Remove empty strings

def create_join_condition(source_keys, target_keys, source_alias='s', target_alias='t'):
    """Create JOIN condition for composite keys"""
    if len(source_keys) != len(target_keys):
        raise ValueError(f"Source keys ({len(source_keys)}) and target keys ({len(target_keys)}) count mismatch")
    
    if not source_keys:
        raise ValueError("No join keys provided")
    
    # Create individual join conditions
    conditions = []
    for source_key, target_key in zip(source_keys, target_keys):
        conditions.append(f"{source_alias}.{source_key} = {target_alias}.{target_key}")
    
    # Join with AND
    return " AND ".join(conditions)

def test_composite_key_functions():
    """Test the composite key parsing and SQL generation"""
    
    print("🧪 Testing Composite Key Functions")
    print("=" * 50)
    
    # Test 1: Single key
    print("\n📝 Test 1: Single Key")
    source_key = "customer_id"
    target_key = "cust_id"
    source_parsed = parse_join_keys(source_key)
    target_parsed = parse_join_keys(target_key)
    join_condition = create_join_condition(source_parsed, target_parsed)
    print(f"Source: {source_key} → {source_parsed}")
    print(f"Target: {target_key} → {target_parsed}")
    print(f"JOIN: {join_condition}")
    
    # Test 2: Two-column composite key
    print("\n📝 Test 2: Two-Column Composite Key")
    source_key = "customer_id,account_type"
    target_key = "cust_id,acct_type"
    source_parsed = parse_join_keys(source_key)
    target_parsed = parse_join_keys(target_key)
    join_condition = create_join_condition(source_parsed, target_parsed)
    print(f"Source: {source_key} → {source_parsed}")
    print(f"Target: {target_key} → {target_parsed}")
    print(f"JOIN: {join_condition}")
    
    # Test 3: Three-column composite key
    print("\n📝 Test 3: Three-Column Composite Key")
    source_key = "region,product_type,quarter"
    target_key = "area,product_line,time_period"
    source_parsed = parse_join_keys(source_key)
    target_parsed = parse_join_keys(target_key)
    join_condition = create_join_condition(source_parsed, target_parsed)
    print(f"Source: {source_key} → {source_parsed}")
    print(f"Target: {target_key} → {target_parsed}")
    print(f"JOIN: {join_condition}")
    
    # Test 4: Same column names
    print("\n📝 Test 4: Same Column Names")
    source_key = "customer_id,account_type"
    target_key = "customer_id,account_type"
    source_parsed = parse_join_keys(source_key)
    target_parsed = parse_join_keys(target_key)
    join_condition = create_join_condition(source_parsed, target_parsed)
    print(f"Source: {source_key} → {source_parsed}")
    print(f"Target: {target_key} → {target_parsed}")
    print(f"JOIN: {join_condition}")
    
    # Test 5: With spaces
    print("\n📝 Test 5: Keys with Spaces")
    source_key = " customer_id , account_type , region "
    target_key = " cust_id , acct_type , area "
    source_parsed = parse_join_keys(source_key)
    target_parsed = parse_join_keys(target_key)
    join_condition = create_join_condition(source_parsed, target_parsed)
    print(f"Source: '{source_key}' → {source_parsed}")
    print(f"Target: '{target_key}' → {target_parsed}")
    print(f"JOIN: {join_condition}")
    
    print("\n✅ All tests completed successfully!")
    
    # Generate sample SQL
    print("\n🔍 Sample SQL with Composite Keys:")
    print("-" * 40)
    
    sample_transformation_sql = f"""
-- Composite Key Validation Example
WITH source_data AS (
    SELECT 
        customer_id,
        account_type,
        SUM(balance) as total_balance
    FROM `project.dataset.customers_source`
    GROUP BY customer_id, account_type
),
target_data AS (
    SELECT 
        cust_id,
        acct_type,
        balance_total
    FROM `project.dataset.account_summary_target`
)
SELECT 
    s.customer_id as source_customer_id,
    s.account_type as source_account_type,
    s.total_balance as source_value,
    t.balance_total as target_value,
    CASE 
        WHEN s.total_balance = t.balance_total THEN 'MATCH'
        ELSE 'MISMATCH'
    END as validation_result
FROM source_data s
FULL OUTER JOIN target_data t 
    ON s.customer_id = t.cust_id AND s.account_type = t.acct_type
ORDER BY s.customer_id, s.account_type;
"""
    
    print(sample_transformation_sql)

if __name__ == "__main__":
    test_composite_key_functions()
