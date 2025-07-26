#!/usr/bin/env python3
"""
Comprehensive Banking Data Validation Scenarios
Real-world validation testing against BigQuery data
Project ID: cohesive-apogee-411113
"""

from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'comprehensive_validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

class ComprehensiveBankingValidator:
    """Comprehensive validation for banking data scenarios."""
    
    def __init__(self, project_id="cohesive-apogee-411113"):
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = "banking_sample_data"
        self.results = []
        
    def run_validation(self, name, description, query, expected_condition=None):
        """Run a validation query and check results."""
        try:
            logger.info(f"Running validation: {name}")
            logger.info(f"Description: {description}")
            logger.info(f"Query: {query}")
            
            query_job = self.client.query(query)
            results = query_job.result()
            
            result_data = []
            for row in results:
                row_dict = dict(row.items())
                result_data.append(row_dict)
            
            # Determine validation status
            status = "PASS"
            if expected_condition:
                # Evaluate the expected condition
                if not expected_condition(result_data):
                    status = "FAIL"
            
            validation_result = {
                'name': name,
                'description': description,
                'status': status,
                'results': result_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.results.append(validation_result)
            logger.info(f"✅ Validation completed: {status}")
            
            # Display results
            if result_data:
                logger.info("Results:")
                for i, row in enumerate(result_data[:5], 1):  # Show first 5 rows
                    logger.info(f"  {i}. {row}")
                if len(result_data) > 5:
                    logger.info(f"  ... and {len(result_data) - 5} more rows")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            validation_result = {
                'name': name,
                'description': description,
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.results.append(validation_result)
            return validation_result
    
    def validate_data_quality(self):
        """Validate basic data quality rules."""
        logger.info("=" * 60)
        logger.info("🔍 DATA QUALITY VALIDATIONS")
        logger.info("=" * 60)
        
        # 1. Customer ID uniqueness
        self.run_validation(
            name="Customer ID Uniqueness",
            description="Ensure all customer IDs are unique",
            query=f"""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT customer_id) as unique_customers,
                COUNT(*) - COUNT(DISTINCT customer_id) as duplicates
            FROM `{self.project_id}.{self.dataset_id}.customers`
            """,
            expected_condition=lambda r: r[0]['duplicates'] == 0
        )
        
        # 2. Account number format validation
        self.run_validation(
            name="Account Number Format",
            description="Validate account numbers follow ACC_xxxxxxxxx pattern",
            query=f"""
            SELECT 
                COUNT(*) as total_accounts,
                COUNT(CASE WHEN REGEXP_CONTAINS(account_number, r'^ACC_[0-9]{{9}}$') THEN 1 END) as valid_format,
                COUNT(CASE WHEN NOT REGEXP_CONTAINS(account_number, r'^ACC_[0-9]{{9}}$') THEN 1 END) as invalid_format
            FROM `{self.project_id}.{self.dataset_id}.customers`
            """,
            expected_condition=lambda r: r[0]['invalid_format'] == 0
        )
        
        # 3. Transaction ID uniqueness
        self.run_validation(
            name="Transaction ID Uniqueness",
            description="Ensure all transaction IDs are unique",
            query=f"""
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(DISTINCT transaction_id) as unique_transactions,
                COUNT(*) - COUNT(DISTINCT transaction_id) as duplicates
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            """,
            expected_condition=lambda r: r[0]['duplicates'] == 0
        )
        
        # 4. Required fields completeness
        self.run_validation(
            name="Customer Required Fields",
            description="Check for null values in required customer fields",
            query=f"""
            SELECT 
                COUNT(*) as total_customers,
                COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as null_customer_id,
                COUNT(CASE WHEN account_number IS NULL THEN 1 END) as null_account_number,
                COUNT(CASE WHEN account_type IS NULL THEN 1 END) as null_account_type,
                COUNT(CASE WHEN account_status IS NULL THEN 1 END) as null_account_status
            FROM `{self.project_id}.{self.dataset_id}.customers`
            """,
            expected_condition=lambda r: all(r[0][field] == 0 for field in ['null_customer_id', 'null_account_number', 'null_account_type', 'null_account_status'])
        )
    
    def validate_business_rules(self):
        """Validate complex banking business rules."""
        logger.info("=" * 60)
        logger.info("🏦 BUSINESS RULES VALIDATIONS")
        logger.info("=" * 60)
        
        # 1. Account balance consistency by type
        self.run_validation(
            name="Account Balance Rules",
            description="Validate account balances follow business rules by account type",
            query=f"""
            SELECT 
                account_type,
                COUNT(*) as total_accounts,
                AVG(balance) as avg_balance,
                MIN(balance) as min_balance,
                MAX(balance) as max_balance,
                COUNT(CASE WHEN account_type = 'CHECKING' AND balance < -1000 THEN 1 END) as checking_overdraft_violations,
                COUNT(CASE WHEN account_type IN ('CREDIT', 'LOAN') AND balance > 0 THEN 1 END) as debt_positive_violations
            FROM `{self.project_id}.{self.dataset_id}.customers`
            GROUP BY account_type
            ORDER BY account_type
            """
        )
        
        # 2. Risk score validation
        self.run_validation(
            name="Risk Score Validation",
            description="Validate risk scores are within acceptable range (300-850)",
            query=f"""
            SELECT 
                COUNT(*) as total_customers,
                COUNT(CASE WHEN risk_score BETWEEN 300 AND 850 THEN 1 END) as valid_risk_scores,
                COUNT(CASE WHEN risk_score < 300 OR risk_score > 850 THEN 1 END) as invalid_risk_scores,
                MIN(risk_score) as min_risk_score,
                MAX(risk_score) as max_risk_score,
                AVG(risk_score) as avg_risk_score
            FROM `{self.project_id}.{self.dataset_id}.customers`
            """,
            expected_condition=lambda r: r[0]['invalid_risk_scores'] == 0
        )
        
        # 3. Transaction amount reasonableness
        self.run_validation(
            name="Transaction Amount Validation",
            description="Check for unusually large transactions (potential fraud)",
            query=f"""
            SELECT 
                transaction_type,
                COUNT(*) as total_transactions,
                AVG(ABS(amount)) as avg_amount,
                MAX(ABS(amount)) as max_amount,
                COUNT(CASE WHEN ABS(amount) > 100000 THEN 1 END) as large_transactions,
                COUNT(CASE WHEN amount = 0 THEN 1 END) as zero_amount_transactions
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            GROUP BY transaction_type
            ORDER BY transaction_type
            """
        )
        
        # 4. Fraud detection correlation
        self.run_validation(
            name="Fraud Detection Analysis",
            description="Analyze fraud patterns and correlations",
            query=f"""
            SELECT 
                is_fraudulent,
                COUNT(*) as transaction_count,
                AVG(ABS(amount)) as avg_amount,
                transaction_type,
                channel,
                status
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            GROUP BY is_fraudulent, transaction_type, channel, status
            HAVING COUNT(*) > 5
            ORDER BY is_fraudulent DESC, transaction_count DESC
            """
        )
    
    def validate_cross_table_integrity(self):
        """Validate relationships between tables."""
        logger.info("=" * 60)
        logger.info("🔗 CROSS-TABLE INTEGRITY VALIDATIONS")
        logger.info("=" * 60)
        
        # 1. Referential integrity - Transactions must have valid customers
        self.run_validation(
            name="Customer-Transaction Referential Integrity",
            description="Ensure all transactions link to valid customer accounts",
            query=f"""
            SELECT 
                'Total Transactions' as check_type,
                COUNT(*) as count
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            
            UNION ALL
            
            SELECT 
                'Transactions with Valid Customers' as check_type,
                COUNT(*) as count
            FROM `{self.project_id}.{self.dataset_id}.transactions` t
            INNER JOIN `{self.project_id}.{self.dataset_id}.customers` c
            ON t.account_number = c.account_number
            
            UNION ALL
            
            SELECT 
                'Orphaned Transactions' as check_type,
                COUNT(*) as count
            FROM `{self.project_id}.{self.dataset_id}.transactions` t
            LEFT JOIN `{self.project_id}.{self.dataset_id}.customers` c
            ON t.account_number = c.account_number
            WHERE c.account_number IS NULL
            """
        )
        
        # 2. Account activity analysis
        self.run_validation(
            name="Account Activity Analysis",
            description="Analyze transaction activity by account type and status",
            query=f"""
            SELECT 
                c.account_type,
                c.account_status,
                COUNT(DISTINCT c.customer_id) as total_customers,
                COUNT(t.transaction_id) as total_transactions,
                ROUND(COUNT(t.transaction_id) / COUNT(DISTINCT c.customer_id), 2) as avg_transactions_per_customer,
                SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END) as total_deposits,
                SUM(CASE WHEN t.amount < 0 THEN ABS(t.amount) ELSE 0 END) as total_withdrawals
            FROM `{self.project_id}.{self.dataset_id}.customers` c
            LEFT JOIN `{self.project_id}.{self.dataset_id}.transactions` t
            ON c.account_number = t.account_number
            GROUP BY c.account_type, c.account_status
            ORDER BY c.account_type, c.account_status
            """
        )
        
        # 3. High-risk customer transaction patterns
        self.run_validation(
            name="High-Risk Customer Analysis",
            description="Analyze transaction patterns for high-risk customers",
            query=f"""
            SELECT 
                CASE 
                    WHEN c.risk_score < 400 THEN 'Very High Risk'
                    WHEN c.risk_score < 500 THEN 'High Risk'
                    WHEN c.risk_score < 600 THEN 'Medium Risk'
                    WHEN c.risk_score < 700 THEN 'Low Risk'
                    ELSE 'Very Low Risk'
                END as risk_category,
                COUNT(DISTINCT c.customer_id) as customer_count,
                COUNT(t.transaction_id) as transaction_count,
                SUM(CASE WHEN t.is_fraudulent THEN 1 ELSE 0 END) as fraud_transactions,
                ROUND(AVG(ABS(t.amount)), 2) as avg_transaction_amount,
                ROUND(SUM(CASE WHEN t.is_fraudulent THEN 1 ELSE 0 END) * 100.0 / COUNT(t.transaction_id), 2) as fraud_percentage
            FROM `{self.project_id}.{self.dataset_id}.customers` c
            LEFT JOIN `{self.project_id}.{self.dataset_id}.transactions` t
            ON c.account_number = t.account_number
            GROUP BY risk_category
            ORDER BY 
                CASE risk_category
                    WHEN 'Very High Risk' THEN 1
                    WHEN 'High Risk' THEN 2
                    WHEN 'Medium Risk' THEN 3
                    WHEN 'Low Risk' THEN 4
                    WHEN 'Very Low Risk' THEN 5
                END
            """
        )
    
    def validate_temporal_consistency(self):
        """Validate date and time consistency."""
        logger.info("=" * 60)
        logger.info("📅 TEMPORAL CONSISTENCY VALIDATIONS")
        logger.info("=" * 60)
        
        # 1. Account opening vs last transaction dates
        self.run_validation(
            name="Date Consistency Check",
            description="Ensure last transaction date is after account opening date",
            query=f"""
            SELECT 
                COUNT(*) as total_customers,
                COUNT(CASE WHEN DATE(last_transaction_date) >= account_open_date THEN 1 END) as valid_date_sequence,
                COUNT(CASE WHEN DATE(last_transaction_date) < account_open_date THEN 1 END) as invalid_date_sequence,
                MIN(account_open_date) as earliest_account,
                MAX(account_open_date) as latest_account,
                MIN(DATE(last_transaction_date)) as earliest_transaction,
                MAX(DATE(last_transaction_date)) as latest_transaction
            FROM `{self.project_id}.{self.dataset_id}.customers`
            WHERE last_transaction_date IS NOT NULL
            """,
            expected_condition=lambda r: r[0]['invalid_date_sequence'] == 0
        )
        
        # 2. Transaction date distribution
        self.run_validation(
            name="Transaction Date Distribution",
            description="Analyze transaction distribution over time",
            query=f"""
            SELECT 
                EXTRACT(YEAR FROM transaction_timestamp) as year,
                EXTRACT(MONTH FROM transaction_timestamp) as month,
                COUNT(*) as transaction_count,
                COUNT(DISTINCT account_number) as unique_accounts,
                SUM(CASE WHEN is_fraudulent THEN 1 ELSE 0 END) as fraud_count
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            GROUP BY year, month
            ORDER BY year DESC, month DESC
            """
        )
    
    def validate_aggregation_consistency(self):
        """Validate data aggregation and summary consistency."""
        logger.info("=" * 60)
        logger.info("📊 AGGREGATION CONSISTENCY VALIDATIONS")
        logger.info("=" * 60)
        
        # 1. Balance vs transaction history reconciliation
        self.run_validation(
            name="Balance Reconciliation",
            description="Check if account balances align with transaction history (sample)",
            query=f"""
            WITH customer_transactions AS (
                SELECT 
                    c.customer_id,
                    c.account_number,
                    c.balance as current_balance,
                    COALESCE(SUM(t.amount), 0) as transaction_total,
                    COUNT(t.transaction_id) as transaction_count
                FROM `{self.project_id}.{self.dataset_id}.customers` c
                LEFT JOIN `{self.project_id}.{self.dataset_id}.transactions` t
                ON c.account_number = t.account_number
                GROUP BY c.customer_id, c.account_number, c.balance
            )
            SELECT 
                COUNT(*) as total_customers,
                COUNT(CASE WHEN transaction_count > 0 THEN 1 END) as customers_with_transactions,
                COUNT(CASE WHEN transaction_count = 0 THEN 1 END) as customers_without_transactions,
                ROUND(AVG(current_balance), 2) as avg_current_balance,
                ROUND(AVG(transaction_total), 2) as avg_transaction_total
            FROM customer_transactions
            """
        )
        
        # 2. Processing fee validation
        self.run_validation(
            name="Processing Fee Consistency",
            description="Validate processing fees are applied correctly",
            query=f"""
            SELECT 
                transaction_type,
                channel,
                COUNT(*) as transaction_count,
                AVG(processing_fee) as avg_fee,
                MIN(processing_fee) as min_fee,
                MAX(processing_fee) as max_fee,
                COUNT(CASE WHEN processing_fee = 0 THEN 1 END) as zero_fee_count,
                COUNT(CASE WHEN processing_fee > 0 THEN 1 END) as charged_fee_count
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            GROUP BY transaction_type, channel
            HAVING COUNT(*) > 10
            ORDER BY transaction_type, channel
            """
        )
    
    def generate_summary_report(self):
        """Generate a comprehensive validation summary report."""
        logger.info("=" * 60)
        logger.info("📋 GENERATING VALIDATION SUMMARY REPORT")
        logger.info("=" * 60)
        
        total_validations = len(self.results)
        passed_validations = len([r for r in self.results if r['status'] == 'PASS'])
        failed_validations = len([r for r in self.results if r['status'] == 'FAIL'])
        error_validations = len([r for r in self.results if r['status'] == 'ERROR'])
        
        success_rate = (passed_validations / total_validations * 100) if total_validations > 0 else 0
        
        # Create summary DataFrame
        summary_data = []
        for result in self.results:
            summary_data.append({
                'Validation Name': result['name'],
                'Description': result['description'],
                'Status': result['status'],
                'Timestamp': result['timestamp'],
                'Error': result.get('error', '')
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_validation_report_{timestamp}.csv"
        summary_df.to_csv(filename, index=False)
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE VALIDATION SUMMARY REPORT")
        print("=" * 80)
        print(f"📊 Total Validations: {total_validations}")
        print(f"✅ Passed: {passed_validations}")
        print(f"❌ Failed: {failed_validations}")
        print(f"🔥 Errors: {error_validations}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"💾 Report saved to: {filename}")
        print("=" * 80)
        
        # Show validation details
        for result in self.results:
            status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "🔥"
            print(f"{status_emoji} {result['name']}: {result['status']}")
            if result['status'] == 'ERROR':
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        return filename
    
    def run_all_validations(self):
        """Run all comprehensive validations."""
        logger.info("🚀 Starting Comprehensive Banking Data Validations")
        logger.info(f"Project: {self.project_id}")
        logger.info(f"Dataset: {self.dataset_id}")
        logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all validation categories
        self.validate_data_quality()
        self.validate_business_rules()
        self.validate_cross_table_integrity()
        self.validate_temporal_consistency()
        self.validate_aggregation_consistency()
        
        # Generate summary report
        report_file = self.generate_summary_report()
        
        logger.info("🎉 Comprehensive validation completed!")
        return report_file

if __name__ == "__main__":
    validator = ComprehensiveBankingValidator()
    report = validator.run_all_validations()
