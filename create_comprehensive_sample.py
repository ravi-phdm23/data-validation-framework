"""
Enhanced Excel Sample Generator with Composite Key Support
This script creates comprehensive validation scenarios including composite keys
"""

import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_comprehensive_excel_sample():
    """Create comprehensive Excel sample with all validation scenarios including composite keys"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Comprehensive_Validation_Scenarios_{timestamp}.xlsx"
    
    # Comprehensive validation scenarios
    validation_scenarios = [
        # Basic transformations
        {
            'Validation_Name': 'Customer Full Name Transformation',
            'Source_Table': 'customers',
            'Target_Table': 'customer_profiles',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
            'Validation_Type': 'TRANSFORMATION',
            'Description': 'Concatenate first and last name from source'
        },
        
        # Different join key names
        {
            'Validation_Name': 'Customer Profile with Different Keys',
            'Source_Table': 'customers_source',
            'Target_Table': 'customer_profiles_target',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'cust_id',
            'Target_Column': 'full_name',
            'Derivation_Logic': 'CONCAT(first_name, " ", last_name)',
            'Validation_Type': 'TRANSFORMATION',
            'Description': 'Source uses customer_id, target uses cust_id'
        },
        
        # Aggregations
        {
            'Validation_Name': 'Total Transaction Amount',
            'Source_Table': 'transactions',
            'Target_Table': 'account_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_number',
            'Target_Column': 'total_transaction_amount',
            'Derivation_Logic': 'SUM(amount)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Sum all transactions per account'
        },
        
        # COMPOSITE KEY SCENARIOS
        {
            'Validation_Name': 'Account Type Summary - Composite Key Test',
            'Source_Table': 'customers',
            'Target_Table': 'account_type_summary',
            'Source_Join_Key': 'customer_id,account_type',
            'Target_Join_Key': 'customer_id,account_type',
            'Target_Column': 'total_balance',
            'Derivation_Logic': 'SUM(balance)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Composite key: customer_id + account_type for balance aggregation'
        },
        
        {
            'Validation_Name': 'Account Summary - Different Composite Keys',
            'Source_Table': 'customers_source',
            'Target_Table': 'account_summary_target',
            'Source_Join_Key': 'customer_id,account_type',
            'Target_Join_Key': 'cust_id,acct_type',
            'Target_Column': 'balance_total',
            'Derivation_Logic': 'SUM(balance)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Source: customer_id+account_type, Target: cust_id+acct_type'
        },
        
        {
            'Validation_Name': 'Regional Analysis - Triple Composite Key',
            'Source_Table': 'transactions',
            'Target_Table': 'regional_analysis',
            'Source_Join_Key': 'region,product_type,quarter',
            'Target_Join_Key': 'region,product_type,quarter',
            'Target_Column': 'total_revenue',
            'Derivation_Logic': 'SUM(amount)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Triple composite key: region + product_type + quarter'
        },
        
        {
            'Validation_Name': 'Regional Product Analysis - Different Triple Keys',
            'Source_Table': 'transactions_extended',
            'Target_Table': 'region_product_target',
            'Source_Join_Key': 'region,product_type,time_period',
            'Target_Join_Key': 'area,product_line,time_period',
            'Target_Column': 'revenue_total',
            'Derivation_Logic': 'SUM(transaction_amount)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Source: region+product_type+time_period, Target: area+product_line+time_period'
        },
        
        # Complex transformations with composite keys
        {
            'Validation_Name': 'Customer Risk Assessment - Composite',
            'Source_Table': 'customers',
            'Target_Table': 'risk_analysis',
            'Source_Join_Key': 'customer_id,risk_segment',
            'Target_Join_Key': 'cust_id,segment',
            'Target_Column': 'risk_score',
            'Derivation_Logic': 'CASE WHEN balance > 50000 THEN 1 WHEN balance > 10000 THEN 2 ELSE 3 END',
            'Validation_Type': 'TRANSFORMATION',
            'Description': 'Risk scoring with composite customer and segment keys'
        },
        
        # Cross-table joins with composite keys
        {
            'Validation_Name': 'Customer Transaction Summary - Multi-Composite',
            'Source_Table': 'customers JOIN transactions ON customers.customer_id = transactions.customer_id',
            'Target_Table': 'customer_transaction_summary',
            'Source_Join_Key': 'customers.customer_id,transactions.account_type',
            'Target_Join_Key': 'cust_id,acct_type',
            'Target_Column': 'avg_monthly_transactions',
            'Derivation_Logic': 'AVG(transactions.amount)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Cross-table aggregation with composite keys from different tables'
        },
        
        # Date-based composite keys
        {
            'Validation_Name': 'Monthly Account Activity - Date Composite',
            'Source_Table': 'transactions',
            'Target_Table': 'monthly_activity',
            'Source_Join_Key': 'account_number,EXTRACT(YEAR FROM transaction_date),EXTRACT(MONTH FROM transaction_date)',
            'Target_Join_Key': 'account_num,year,month',
            'Target_Column': 'monthly_total',
            'Derivation_Logic': 'SUM(amount)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Composite key with date components: account + year + month'
        },
        
        # Additional standard scenarios
        {
            'Validation_Name': 'Transaction Count per Account',
            'Source_Table': 'transactions',
            'Target_Table': 'account_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_number',
            'Target_Column': 'transaction_count',
            'Derivation_Logic': 'COUNT(*)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Count transactions per account'
        },
        
        {
            'Validation_Name': 'Customer Risk Level',
            'Source_Table': 'customers',
            'Target_Table': 'customer_profiles',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'risk_level',
            'Derivation_Logic': 'CASE WHEN balance > 50000 THEN "LOW" WHEN balance > 10000 THEN "MEDIUM" ELSE "HIGH" END',
            'Validation_Type': 'TRANSFORMATION',
            'Description': 'Risk categorization based on balance'
        },
        
        {
            'Validation_Name': 'Account Status Flag',
            'Source_Table': 'customers',
            'Target_Table': 'customer_profiles',
            'Source_Join_Key': 'customer_id',
            'Target_Join_Key': 'customer_id',
            'Target_Column': 'account_status',
            'Derivation_Logic': 'CASE WHEN balance > 0 THEN "ACTIVE" ELSE "INACTIVE" END',
            'Validation_Type': 'TRANSFORMATION',
            'Description': 'Active/Inactive based on balance'
        },
        
        {
            'Validation_Name': 'Average Transaction Amount',
            'Source_Table': 'transactions',
            'Target_Table': 'account_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_number',
            'Target_Column': 'avg_transaction_amount',
            'Derivation_Logic': 'AVG(amount)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Average transaction amount per account'
        },
        
        {
            'Validation_Name': 'Latest Transaction Date',
            'Source_Table': 'transactions',
            'Target_Table': 'account_summary',
            'Source_Join_Key': 'account_number',
            'Target_Join_Key': 'account_number',
            'Target_Column': 'latest_transaction_date',
            'Derivation_Logic': 'MAX(transaction_date)',
            'Validation_Type': 'AGGREGATION',
            'Description': 'Most recent transaction date per account'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(validation_scenarios)
    
    # Create documentation sheet
    documentation_data = [
        ['COMPOSITE KEY SUPPORT', 'This template now supports composite primary keys'],
        ['', ''],
        ['Source_Join_Key Format', 'For single key: customer_id'],
        ['', 'For composite key: customer_id,account_type'],
        ['', 'For triple key: region,product_type,quarter'],
        ['', ''],
        ['Target_Join_Key Format', 'Same format as Source_Join_Key'],
        ['', 'Can have different column names than source'],
        ['', 'Example: customer_id,account_type → cust_id,acct_type'],
        ['', ''],
        ['COMPOSITE KEY EXAMPLES', ''],
        ['Two-Column Composite', 'customer_id,account_type'],
        ['Three-Column Composite', 'region,product_type,quarter'],
        ['Date-Based Composite', 'account_number,year,month'],
        ['Cross-Table Composite', 'customers.customer_id,transactions.account_type'],
        ['', ''],
        ['VALIDATION TYPES', ''],
        ['TRANSFORMATION', 'Single-row calculations, CASE statements, string functions'],
        ['AGGREGATION', 'SUM, COUNT, AVG, MAX, MIN with GROUP BY'],
        ['', ''],
        ['DERIVATION LOGIC EXAMPLES', ''],
        ['Simple Transformation', 'CONCAT(first_name, " ", last_name)'],
        ['Conditional Logic', 'CASE WHEN balance > 50000 THEN "LOW" ELSE "HIGH" END'],
        ['Aggregation', 'SUM(amount)'],
        ['Date Function', 'EXTRACT(YEAR FROM transaction_date)'],
        ['', ''],
        ['COMPOSITE KEY SQL GENERATION', ''],
        ['Source Join Key', 'customer_id,account_type'],
        ['Target Join Key', 'cust_id,acct_type'],
        ['Generated JOIN', 'ON s.customer_id = t.cust_id AND s.account_type = t.acct_type'],
        ['', ''],
        ['BEST PRACTICES', ''],
        ['Column Order', 'Keep same order in source and target composite keys'],
        ['Data Types', 'Ensure matching data types for join columns'],
        ['Null Handling', 'Consider NULL values in composite key columns'],
        ['Performance', 'Create indexes on composite key columns in BigQuery']
    ]
    
    doc_df = pd.DataFrame(documentation_data, columns=['Item', 'Description'])
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Validation_Scenarios', index=False)
        doc_df.to_excel(writer, sheet_name='Composite_Key_Guide', index=False)
        
        # Adjust column widths for better readability
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    logging.info(f"✅ Created comprehensive Excel sample: {filename}")
    logging.info(f"📊 Total scenarios: {len(validation_scenarios)}")
    logging.info(f"🔗 Composite key scenarios: {len([s for s in validation_scenarios if ',' in s['Source_Join_Key']])}")
    
    return filename

if __name__ == "__main__":
    filename = create_comprehensive_excel_sample()
    print(f"Created: {filename}")
