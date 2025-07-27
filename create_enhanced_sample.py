#!/usr/bin/env python3
"""
Create Enhanced Sample Excel File with Reference Table Scenarios
This demonstrates the new VLOOKUP, IF-THEN-ELSE, and multi-table validation capabilities.
"""

import pandas as pd
from datetime import datetime

def create_enhanced_sample_excel():
    """Create enhanced sample Excel with reference table scenarios."""
    
    # Enhanced validation scenarios with reference table support
    enhanced_scenarios = pd.DataFrame([
        {
            'Scenario_Name': 'Interest_Rate_VLOOKUP',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'applicable_rate',
            'Derivation_Logic': 'VLOOKUP(account_type, interest_rates)',
            'Reference_Table': 'interest_rates',
            'Reference_Join_Key': 'account_type',
            'Reference_Lookup_Column': 'account_type',
            'Reference_Return_Column': 'rate_value',
            'Business_Conditions': '',
            'Hardcoded_Values': '',
            'Validation_Type': 'VLOOKUP',
            'Business_Rule': 'Lookup applicable interest rate based on account type'
        },
        {
            'Scenario_Name': 'Customer_Tier_Classification',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'customer_tier',
            'Derivation_Logic': 'IF(balance > 100000, "PREMIUM", IF(balance > 50000, "GOLD", "STANDARD"))',
            'Reference_Table': '',
            'Reference_Join_Key': '',
            'Reference_Lookup_Column': '',
            'Reference_Return_Column': '',
            'Business_Conditions': 'balance > 100000 THEN PREMIUM; balance > 50000 THEN GOLD; ELSE STANDARD',
            'Hardcoded_Values': 'PREMIUM=VIP Service,GOLD=Priority Service,STANDARD=Regular Service',
            'Validation_Type': 'Conditional_Logic',
            'Business_Rule': 'Classify customers into tiers based on account balance'
        },
        {
            'Scenario_Name': 'Risk_Score_with_Reference',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary', 
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'risk_category',
            'Derivation_Logic': 'CASE WHEN balance <= 10000 THEN "LOW" WHEN balance <= 50000 THEN "MEDIUM" WHEN balance <= 100000 THEN "HIGH" ELSE "PREMIUM" END',
            'Reference_Table': 'risk_categories',
            'Reference_Join_Key': 'balance_range',
            'Reference_Lookup_Column': 'balance_range',
            'Reference_Return_Column': 'risk_score',
            'Business_Conditions': 'balance <= 10000 THEN LOW; balance <= 50000 THEN MEDIUM; balance <= 100000 THEN HIGH; ELSE PREMIUM',
            'Hardcoded_Values': 'LOW=Low Risk Profile,MEDIUM=Moderate Risk Profile,HIGH=High Risk Profile,PREMIUM=Premium Risk Profile',
            'Validation_Type': 'Range_Based_Lookup',
            'Business_Rule': 'Categorize customers by balance ranges and lookup risk scores from reference table'
        },
        {
            'Scenario_Name': 'Transaction_Fee_Calculation',
            'Source_Table': 'transactions',
            'Target_Table': 'transaction_summary',
            'Source_Join_Key': 'transaction_type',
            'Target_Join_Key': 'transaction_type',
            'Target_Column': 'calculated_fee',
            'Derivation_Logic': 'SOURCE.amount * REFERENCE.fee_percentage',
            'Reference_Table': 'fee_structure',
            'Reference_Join_Key': 'transaction_type',
            'Reference_Lookup_Column': 'transaction_type',
            'Reference_Return_Column': 'fee_percentage',
            'Business_Conditions': 'amount > 10000 THEN fee_percentage * 0.5; ELSE fee_percentage',
            'Hardcoded_Values': '',
            'Validation_Type': 'Multi_Table_Calculation',
            'Business_Rule': 'Calculate transaction fees based on type and amount with volume discounts'
        },
        {
            'Scenario_Name': 'Account_Status_Complex_Logic',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id', 
            'Target_Column': 'account_status_derived',
            'Derivation_Logic': 'IF(balance > 0 AND transaction_count > 5, "ACTIVE", IF(balance > 0, "DORMANT", "INACTIVE"))',
            'Reference_Table': 'customer_activity',
            'Reference_Join_Key': 'customer_id',
            'Reference_Lookup_Column': 'customer_id',
            'Reference_Return_Column': 'transaction_count',
            'Business_Conditions': 'balance > 0 AND transaction_count > 5 THEN ACTIVE; balance > 0 THEN DORMANT; ELSE INACTIVE',
            'Hardcoded_Values': 'ACTIVE=Full Access,DORMANT=Limited Access,INACTIVE=No Access',
            'Validation_Type': 'Complex_Conditional',
            'Business_Rule': 'Determine account status based on balance and activity from reference table'
        },
        {
            'Scenario_Name': 'Credit_Limit_Lookup',
            'Source_Table': 'customers',
            'Target_Table': 'customer_summary',
            'Source_Join_Key': 'customer_id,account_type',
            'Target_Join_Key': 'customer_id,account_type',
            'Target_Column': 'approved_credit_limit',
            'Derivation_Logic': 'VLOOKUP(account_type + income_tier, credit_limits)',
            'Reference_Table': 'credit_limits',
            'Reference_Join_Key': 'account_type,income_tier',
            'Reference_Lookup_Column': 'account_type,income_tier',
            'Reference_Return_Column': 'max_credit_limit',
            'Business_Conditions': 'monthly_income > 10000 THEN HIGH_INCOME; monthly_income > 5000 THEN MID_INCOME; ELSE LOW_INCOME',
            'Hardcoded_Values': 'HIGH_INCOME=Tier1,MID_INCOME=Tier2,LOW_INCOME=Tier3',
            'Validation_Type': 'Composite_Key_Lookup',
            'Business_Rule': 'Lookup credit limit based on account type and derived income tier'
        },
        {
            'Scenario_Name': 'Compliance_Flag_Multi_Conditions',
            'Source_Table': 'customers',
            'Target_Table': 'compliance_summary',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'compliance_status',
            'Derivation_Logic': 'CASE WHEN balance >= 100000 THEN "KYC_003" WHEN balance >= 50000 THEN "KYC_002" ELSE "KYC_001" END',
            'Reference_Table': 'compliance_rules',
            'Reference_Join_Key': 'rule_id',
            'Reference_Lookup_Column': 'rule_id',
            'Reference_Return_Column': 'compliance_level',
            'Business_Conditions': 'balance >= 100000 THEN KYC_003; balance >= 50000 THEN KYC_002; ELSE KYC_001',
            'Hardcoded_Values': 'KYC_003=Premium Compliance,KYC_002=Enhanced Compliance,KYC_001=Basic Compliance',
            'Validation_Type': 'Range_Based_Compliance',
            'Business_Rule': 'Determine compliance level based on customer balance thresholds'
        },
        {
            'Scenario_Name': 'Product_Eligibility_Matrix',
            'Source_Table': 'customers',
            'Target_Table': 'product_eligibility',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'eligible_products',
            'Derivation_Logic': 'VLOOKUP(account_type + tier, product_matrix)',
            'Reference_Table': 'product_matrix',
            'Reference_Join_Key': 'account_type,customer_tier',
            'Reference_Lookup_Column': 'account_type,customer_tier',
            'Reference_Return_Column': 'product_code',
            'Business_Conditions': 'balance > 100000 THEN PLATINUM; balance > 75000 THEN GOLD; balance > 25000 THEN SILVER; ELSE BRONZE',
            'Hardcoded_Values': 'PLATINUM=All Products Available,GOLD=Premium Products,SILVER=Standard Products,BRONZE=Basic Products',
            'Validation_Type': 'Multi_Key_Lookup',
            'Business_Rule': 'Match customer account type and tier to available products'
        }
    ])
    
    # Reference table examples to show structure
    interest_rates_ref = pd.DataFrame([
        {'account_type': 'SAVINGS', 'rate_value': 0.025, 'description': 'Standard Savings Rate'},
        {'account_type': 'CHECKING', 'rate_value': 0.01, 'description': 'Basic Checking Rate'},
        {'account_type': 'PREMIUM', 'rate_value': 0.045, 'description': 'Premium Account Rate'},
        {'account_type': 'BUSINESS', 'rate_value': 0.035, 'description': 'Business Account Rate'}
    ])
    
    fee_structure_ref = pd.DataFrame([
        {'transaction_type': 'TRANSFER', 'fee_percentage': 0.001, 'min_fee': 1.0, 'max_fee': 50.0},
        {'transaction_type': 'WITHDRAWAL', 'fee_percentage': 0.002, 'min_fee': 2.0, 'max_fee': 25.0},
        {'transaction_type': 'DEPOSIT', 'fee_percentage': 0.0, 'min_fee': 0.0, 'max_fee': 0.0},
        {'transaction_type': 'PAYMENT', 'fee_percentage': 0.0015, 'min_fee': 1.5, 'max_fee': 75.0}
    ])
    
    # Instructions for enhanced features
    enhanced_instructions = pd.DataFrame([
        {'Feature': 'VLOOKUP', 'Description': 'Use Reference_Table, Reference_Join_Key, Reference_Return_Column', 'Example': 'Lookup interest rates by account type'},
        {'Feature': 'Conditional Logic', 'Description': 'Use Business_Conditions with IF-THEN-ELSE patterns', 'Example': 'Customer tier based on balance ranges'},
        {'Feature': 'Hardcoded Values', 'Description': 'Define static mappings with key=value pairs', 'Example': 'PREMIUM=0.05,STANDARD=0.03'},
        {'Feature': 'Multi-table Joins', 'Description': 'Use SOURCE. and REFERENCE. prefixes in Derivation_Logic', 'Example': 'SOURCE.amount * REFERENCE.rate'},
        {'Feature': 'Composite Keys', 'Description': 'Use comma-separated keys for complex joins', 'Example': 'customer_id,account_type'},
        {'Feature': 'Complex Conditions', 'Description': 'Combine multiple conditions with AND/OR', 'Example': 'balance > 50000 AND transaction_count > 10'},
        {'Note': 'Backward Compatibility', 'Description': 'All existing scenarios still work', 'Example': 'SUM(amount) GROUP_BY account_number'},
        {'Note': 'Error Handling', 'Description': 'System provides detailed error messages for debugging', 'Example': 'Failed reference table joins show specific error details'}
    ])
    
    # Create Excel file with multiple sheets
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'Enhanced_BigQuery_Validation_Scenarios_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main scenarios with enhanced features
        enhanced_scenarios.to_excel(writer, sheet_name='Enhanced_Scenarios', index=False)
        
        # Reference table examples
        interest_rates_ref.to_excel(writer, sheet_name='Sample_Interest_Rates', index=False)
        fee_structure_ref.to_excel(writer, sheet_name='Sample_Fee_Structure', index=False)
        
        # Enhanced feature guide
        enhanced_instructions.to_excel(writer, sheet_name='Enhanced_Features_Guide', index=False)
        
        # Original format for backward compatibility
        original_scenarios = pd.DataFrame([
            {
                'Scenario_Name': 'Original_Balance_Validation',
                'Source_Table': 'customers',
                'Target_Table': 'customers',
                'Source_Join_Key': 'customer_id',
                'Target_Join_Key': 'customer_id',
                'Target_Column': 'balance',
                'Derivation_Logic': 'balance',
                'Validation_Type': 'Data_Quality',
                'Business_Rule': 'Validate customer balance values'
            },
            {
                'Scenario_Name': 'Original_Transaction_Count',
                'Source_Table': 'transactions',
                'Target_Table': 'transactions',
                'Source_Join_Key': 'account_number',
                'Target_Join_Key': 'account_number',
                'Target_Column': 'transaction_count',
                'Derivation_Logic': 'COUNT(*) GROUP_BY account_number',
                'Validation_Type': 'Aggregation',
                'Business_Rule': 'Count transactions per account'
            }
        ])
        original_scenarios.to_excel(writer, sheet_name='Original_Format_Examples', index=False)
    
    print(f"✅ Enhanced sample Excel file created: {filename}")
    print("\n🆕 New Enhanced Features:")
    print("1. VLOOKUP operations with reference tables")
    print("2. IF-THEN-ELSE conditional logic with hardcoded values")
    print("3. Multi-table JOIN operations")
    print("4. Composite key support")
    print("5. Complex business condition parsing")
    print("6. Reference table integration")
    
    return filename

if __name__ == "__main__":
    create_enhanced_sample_excel()
