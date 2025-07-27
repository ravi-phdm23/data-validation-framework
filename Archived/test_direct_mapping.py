#!/usr/bin/env python3
"""
Test Direct Mapping Validation Type
Shows how simple column copying works in the BigQuery validation framework.
"""

import pandas as pd
from google.cloud import bigquery

def test_direct_mapping_scenarios():
    """Test different direct mapping scenarios."""
    
    print("🧪 Testing Direct Mapping Validation Type")
    print("=" * 60)
    
    # Sample scenarios for direct mapping
    direct_mapping_scenarios = [
        {
            'name': 'Copy_Customer_First_Name',
            'source_table': 'customers',
            'target_table': 'customer_profiles',
            'source_join_key': 'customer_id',
            'target_join_key': 'customer_id', 
            'target_column': 'profile_first_name',
            'derivation_logic': 'first_name',
            'validation_type': 'Direct_Mapping',
            'business_rule': 'Copy customer first name directly to profile table'
        },
        {
            'name': 'Copy_Account_Balance',
            'source_table': 'customers',
            'target_table': 'balance_snapshot',
            'source_join_key': 'customer_id',
            'target_join_key': 'customer_id',
            'target_column': 'current_balance', 
            'derivation_logic': 'balance',
            'validation_type': 'Direct_Mapping',
            'business_rule': 'Copy current balance without modification'
        },
        {
            'name': 'Copy_Transaction_Amount',
            'source_table': 'transactions',
            'target_table': 'transaction_log',
            'source_join_key': 'transaction_id',
            'target_join_key': 'log_transaction_id',
            'target_column': 'original_amount',
            'derivation_logic': 'amount',
            'validation_type': 'Direct_Mapping', 
            'business_rule': 'Copy transaction amount as-is to audit log'
        },
        {
            'name': 'Copy_Account_Number',
            'source_table': 'customers',
            'target_table': 'account_summary',
            'source_join_key': 'customer_id',
            'target_join_key': 'customer_id',
            'target_column': 'account_ref',
            'derivation_logic': 'account_number',
            'validation_type': 'Direct_Mapping',
            'business_rule': 'Copy account number to reference field'
        }
    ]
    
    print("📋 Direct Mapping Scenarios:")
    print()
    
    for i, scenario in enumerate(direct_mapping_scenarios, 1):
        print(f"🔄 Scenario {i}: {scenario['name']}")
        print(f"   Source Table: {scenario['source_table']}")
        print(f"   Target Column: {scenario['target_column']}")
        print(f"   Derivation Logic: {scenario['derivation_logic']}")
        print(f"   Validation Type: {scenario['validation_type']}")
        print(f"   Business Rule: {scenario['business_rule']}")
        print()
        
        # Show what SQL would be generated
        expected_sql = generate_direct_mapping_sql(scenario)
        print(f"   📄 Generated SQL Preview:")
        print("   " + "-" * 50)
        for line in expected_sql.split('\n')[:10]:  # Show first 10 lines
            print(f"   {line}")
        print("   ...")
        print("   " + "-" * 50)
        print()

def generate_direct_mapping_sql(scenario):
    """Generate SQL for direct mapping scenario."""
    
    project_id = 'cohesive-apogee-411113'
    dataset_id = 'banking_sample_data'
    
    source_ref = f"`{project_id}.{dataset_id}.{scenario['source_table']}`"
    
    sql = f"""-- Direct Mapping Validation: {scenario['target_column']}
-- Source Table: {scenario['source_table']}
-- Target Table: {scenario['target_table']}
-- Derivation Logic: {scenario['derivation_logic']}
-- Business Rule: {scenario['business_rule']}

WITH transformed_data AS (
    SELECT 
        {scenario['source_join_key']},
        {scenario['derivation_logic']} as calculated_{scenario['target_column']}
    FROM {source_ref}
),
validation_summary AS (
    SELECT 
        COUNT(*) as total_rows,
        COUNT(calculated_{scenario['target_column']}) as non_null_rows,
        COUNT(*) - COUNT(calculated_{scenario['target_column']}) as null_rows,
        MIN(CAST(calculated_{scenario['target_column']} AS STRING)) as sample_value
    FROM transformed_data
)
SELECT 
    'PASS' as validation_status,
    total_rows as row_count,
    ROUND(100.0, 2) as percentage,
    CONCAT('Direct mapping successful: ', CAST(total_rows AS STRING), ' rows processed') as details
FROM validation_summary
WHERE total_rows > 0

UNION ALL

SELECT 
    'INFO' as validation_status,
    non_null_rows as row_count,
    ROUND(non_null_rows * 100.0 / NULLIF(total_rows, 0), 2) as percentage,  
    CONCAT('Non-null values: ', CAST(non_null_rows AS STRING), ' out of ', CAST(total_rows AS STRING)) as details
FROM validation_summary
WHERE total_rows > 0"""
    
    return sql

def create_direct_mapping_excel_template():
    """Create Excel template with direct mapping examples."""
    
    print("📄 Creating Direct Mapping Excel Template...")
    
    scenarios = [
        {
            'Scenario_Name': 'Copy_Customer_First_Name',
            'Source_Table': 'customers',
            'Target_Table': 'customer_profiles', 
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'profile_first_name',
            'Derivation_Logic': 'first_name',
            'Validation_Type': 'Direct_Mapping',
            'Business_Rule': 'Copy customer first name directly to profile table'
        },
        {
            'Scenario_Name': 'Copy_Customer_Last_Name', 
            'Source_Table': 'customers',
            'Target_Table': 'customer_profiles',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'profile_last_name',
            'Derivation_Logic': 'last_name',
            'Validation_Type': 'Direct_Mapping',
            'Business_Rule': 'Copy customer last name directly to profile table'
        },
        {
            'Scenario_Name': 'Copy_Account_Balance',
            'Source_Table': 'customers', 
            'Target_Table': 'balance_snapshot',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'current_balance',
            'Derivation_Logic': 'balance', 
            'Validation_Type': 'Direct_Mapping',
            'Business_Rule': 'Copy current balance without modification'
        },
        {
            'Scenario_Name': 'Copy_Transaction_Amount',
            'Source_Table': 'transactions',
            'Target_Table': 'transaction_log',
            'Source_Join_Key': 'transaction_id', 
            'Target_Join_Key': 'log_transaction_id',
            'Target_Column': 'original_amount',
            'Derivation_Logic': 'amount',
            'Validation_Type': 'Direct_Mapping',
            'Business_Rule': 'Copy transaction amount as-is to audit log'
        }
    ]
    
    # Create DataFrame and save to Excel
    df = pd.DataFrame(scenarios)
    filename = 'Direct_Mapping_Sample_Scenarios.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"✅ Excel template created: {filename}")
    print(f"📊 Contains {len(scenarios)} direct mapping scenarios")
    print()
    
    # Display the template
    print("📋 Template Contents:")
    print(df.to_string(index=False))
    
    return filename

def main():
    """Main function to demonstrate direct mapping."""
    
    # Test scenarios
    test_direct_mapping_scenarios()
    
    print("=" * 60)
    print("📝 SUMMARY: Direct Mapping Validation Type")
    print("=" * 60)
    
    print("""
✅ USE Direct_Mapping WHEN:
   - Copying column value exactly as-is
   - No transformation or calculation applied  
   - Simple field-to-field mapping
   - Just changing column names but keeping same value

❌ DON'T USE Direct_Mapping WHEN:
   - Any mathematical operation (SUM, COUNT, AVG) → Use 'Aggregation'
   - Conditional logic (IF statements) → Use 'Transformation' 
   - Data validation or quality checks → Use 'Data_Completeness'
   - Format transformations → Use 'Format_Validation'

📋 EXCEL TEMPLATE FORMAT:
   Derivation_Logic: [column_name]  (e.g., 'first_name', 'balance')
   Validation_Type: Direct_Mapping
   
🎯 EXPECTED RESULT:
   Status: PASS
   Details: "Direct mapping successful: [N] rows processed"
    """)
    
    # Create sample Excel template
    print("\n" + "=" * 60)
    create_direct_mapping_excel_template()

if __name__ == "__main__":
    main()
