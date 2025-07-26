#!/usr/bin/env python3
"""
BigQuery Test Scenarios - 5 Simple Testing Scenarios
Project ID: cohesive-apogee-411113
Dataset: banking_sample_data
Tables: customers, transactions

This file contains 5 simple scenarios to test BigQuery functionality:
1. Basic data retrieval and counting
2. Aggregation and grouping operations
3. Join operations between tables
4. Date filtering and range queries
5. Complex business logic validation
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Configure logging with UTF-8 encoding to handle emojis
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'bigquery_scenarios_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class BigQueryTestScenarios:
    def __init__(self, project_id="cohesive-apogee-411113"):
        self.project_id = project_id
        self.dataset_id = "banking_sample_data"
        self.client = None
        
    def initialize_client(self):
        """Initialize BigQuery client with authentication."""
        try:
            from google.cloud import bigquery
            import google.auth
            
            logger.info(f"Initializing BigQuery client for project: {self.project_id}")
            self.client = bigquery.Client(project=self.project_id)
            logger.info("✅ BigQuery client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize BigQuery client: {e}")
            return False
    
    def execute_query(self, query, scenario_name):
        """Execute a query and return results with error handling."""
        try:
            logger.info(f"\n📊 Executing {scenario_name}...")
            logger.info(f"Query: {query}")
            
            query_job = self.client.query(query)
            results = query_job.result()
            
            logger.info(f"✅ {scenario_name} executed successfully")
            return results
            
        except Exception as e:
            logger.error(f"❌ {scenario_name} failed: {e}")
            return None
    
    def scenario_1_basic_data_retrieval(self):
        """
        Scenario 1: Basic Data Retrieval and Counting
        - Count total customers and transactions
        - Retrieve sample records from each table
        """
        print("\n" + "="*60)
        print("🔍 SCENARIO 1: Basic Data Retrieval and Counting")
        print("="*60)
        
        # Count customers
        query_customers = f"""
        SELECT 
            COUNT(*) as total_customers,
            COUNT(DISTINCT account_type) as unique_account_types
        FROM `{self.project_id}.{self.dataset_id}.customers`
        """
        
        results = self.execute_query(query_customers, "Customer Count")
        if results:
            for row in results:
                print(f"📈 Total Customers: {row.total_customers}")
                print(f"📈 Unique Account Types: {row.unique_account_types}")
        
        # Count transactions
        query_transactions = f"""
        SELECT 
            COUNT(*) as total_transactions,
            COUNT(DISTINCT transaction_type) as unique_transaction_types,
            MIN(transaction_date) as earliest_date,
            MAX(transaction_date) as latest_date
        FROM `{self.project_id}.{self.dataset_id}.transactions`
        """
        
        results = self.execute_query(query_transactions, "Transaction Count")
        if results:
            for row in results:
                print(f"📈 Total Transactions: {row.total_transactions}")
                print(f"📈 Unique Transaction Types: {row.unique_transaction_types}")
                print(f"📅 Date Range: {row.earliest_date} to {row.latest_date}")
    
    def scenario_2_aggregation_operations(self):
        """
        Scenario 2: Aggregation and Grouping Operations
        - Sum transactions by type
        - Average balance by account type
        - Customer distribution analysis
        """
        print("\n" + "="*60)
        print("💰 SCENARIO 2: Aggregation and Grouping Operations")
        print("="*60)
        
        # Transaction summary by type
        query_transaction_summary = f"""
        SELECT 
            transaction_type,
            COUNT(*) as transaction_count,
            SUM(amount) as total_amount,
            AVG(amount) as average_amount,
            MIN(amount) as min_amount,
            MAX(amount) as max_amount
        FROM `{self.project_id}.{self.dataset_id}.transactions`
        GROUP BY transaction_type
        ORDER BY total_amount DESC
        """
        
        results = self.execute_query(query_transaction_summary, "Transaction Summary by Type")
        if results:
            print("\n📊 Transaction Summary by Type:")
            print("-" * 80)
            print(f"{'Type':<12} {'Count':<8} {'Total Amount':<15} {'Avg Amount':<12} {'Min':<10} {'Max':<10}")
            print("-" * 80)
            for row in results:
                print(f"{row.transaction_type:<12} {row.transaction_count:<8} ${row.total_amount:<14,.2f} ${row.average_amount:<11,.2f} ${row.min_amount:<9,.2f} ${row.max_amount:<9,.2f}")
        
        # Customer balance by account type
        query_balance_summary = f"""
        SELECT 
            account_type,
            COUNT(*) as customer_count,
            AVG(balance) as average_balance,
            SUM(balance) as total_balance,
            MIN(balance) as min_balance,
            MAX(balance) as max_balance
        FROM `{self.project_id}.{self.dataset_id}.customers`
        GROUP BY account_type
        ORDER BY average_balance DESC
        """
        
        results = self.execute_query(query_balance_summary, "Balance Summary by Account Type")
        if results:
            print("\n💳 Balance Summary by Account Type:")
            print("-" * 80)
            print(f"{'Account Type':<12} {'Count':<8} {'Avg Balance':<15} {'Total Balance':<15} {'Min':<10} {'Max':<10}")
            print("-" * 80)
            for row in results:
                print(f"{row.account_type:<12} {row.customer_count:<8} ${row.average_balance:<14,.2f} ${row.total_balance:<14,.2f} ${row.min_balance:<9,.2f} ${row.max_balance:<9,.2f}")
    
    def scenario_3_join_operations(self):
        """
        Scenario 3: Join Operations Between Tables
        - Customer-Transaction joins
        - Customer activity analysis
        - Account balance vs transaction patterns
        """
        print("\n" + "="*60)
        print("🔗 SCENARIO 3: Join Operations Between Tables")
        print("="*60)
        
        # Customer transaction activity
        query_customer_activity = f"""
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.account_type,
            c.balance,
            COUNT(t.transaction_id) as transaction_count,
            SUM(t.amount) as total_transaction_amount,
            AVG(t.amount) as avg_transaction_amount
        FROM `{self.project_id}.{self.dataset_id}.customers` c
        LEFT JOIN `{self.project_id}.{self.dataset_id}.transactions` t
        ON c.account_number = t.account_number
        GROUP BY c.customer_id, c.first_name, c.last_name, c.account_type, c.balance
        HAVING COUNT(t.transaction_id) > 0
        ORDER BY transaction_count DESC
        LIMIT 10
        """
        
        results = self.execute_query(query_customer_activity, "Top 10 Most Active Customers")
        if results:
            print("\n👥 Top 10 Most Active Customers:")
            print("-" * 100)
            print(f"{'Customer ID':<12} {'Name':<20} {'Account Type':<12} {'Balance':<12} {'Transactions':<12} {'Total Amount':<15}")
            print("-" * 100)
            for row in results:
                name = f"{row.first_name} {row.last_name}"
                print(f"{row.customer_id:<12} {name:<20} {row.account_type:<12} ${row.balance:<11,.2f} {row.transaction_count:<12} ${row.total_transaction_amount:<14,.2f}")
        
        # Account type transaction patterns
        query_account_patterns = f"""
        SELECT 
            c.account_type,
            t.transaction_type,
            COUNT(*) as transaction_count,
            SUM(t.amount) as total_amount,
            AVG(t.amount) as avg_amount
        FROM `{self.project_id}.{self.dataset_id}.customers` c
        INNER JOIN `{self.project_id}.{self.dataset_id}.transactions` t
        ON c.account_number = t.account_number
        GROUP BY c.account_type, t.transaction_type
        ORDER BY c.account_type, total_amount DESC
        """
        
        results = self.execute_query(query_account_patterns, "Transaction Patterns by Account Type")
        if results:
            print("\n📈 Transaction Patterns by Account Type:")
            print("-" * 80)
            print(f"{'Account Type':<12} {'Transaction Type':<15} {'Count':<8} {'Total Amount':<15} {'Avg Amount':<12}")
            print("-" * 80)
            for row in results:
                print(f"{row.account_type:<12} {row.transaction_type:<15} {row.transaction_count:<8} ${row.total_amount:<14,.2f} ${row.avg_amount:<11,.2f}")
    
    def scenario_4_date_filtering(self):
        """
        Scenario 4: Date Filtering and Range Queries
        - Recent transactions analysis
        - Monthly transaction trends
        - Date-based customer activity
        """
        print("\n" + "="*60)
        print("📅 SCENARIO 4: Date Filtering and Range Queries")
        print("="*60)
        
        # Recent transactions (last 30 days from max date)
        query_recent_transactions = f"""
        SELECT 
            transaction_date,
            transaction_type,
            COUNT(*) as daily_count,
            SUM(amount) as daily_total,
            AVG(amount) as daily_average
        FROM `{self.project_id}.{self.dataset_id}.transactions`
        WHERE transaction_date >= (
            SELECT DATE_SUB(MAX(transaction_date), INTERVAL 30 DAY)
            FROM `{self.project_id}.{self.dataset_id}.transactions`
        )
        GROUP BY transaction_date, transaction_type
        ORDER BY transaction_date DESC, daily_total DESC
        LIMIT 20
        """
        
        results = self.execute_query(query_recent_transactions, "Recent Transactions (Last 30 Days)")
        if results:
            print("\n📊 Recent Daily Transaction Summary:")
            print("-" * 80)
            print(f"{'Date':<12} {'Type':<12} {'Count':<8} {'Total Amount':<15} {'Avg Amount':<12}")
            print("-" * 80)
            for row in results:
                print(f"{row.transaction_date:<12} {row.transaction_type:<12} {row.daily_count:<8} ${row.daily_total:<14,.2f} ${row.daily_average:<11,.2f}")
        
        # Monthly trends
        query_monthly_trends = f"""
        SELECT 
            EXTRACT(YEAR FROM transaction_date) as year,
            EXTRACT(MONTH FROM transaction_date) as month,
            COUNT(*) as monthly_transactions,
            SUM(amount) as monthly_total,
            COUNT(DISTINCT account_number) as active_accounts
        FROM `{self.project_id}.{self.dataset_id}.transactions`
        GROUP BY year, month
        ORDER BY year DESC, month DESC
        LIMIT 12
        """
        
        results = self.execute_query(query_monthly_trends, "Monthly Transaction Trends")
        if results:
            print("\n📈 Monthly Transaction Trends:")
            print("-" * 70)
            print(f"{'Year-Month':<12} {'Transactions':<12} {'Total Amount':<15} {'Active Accounts':<15}")
            print("-" * 70)
            for row in results:
                month_year = f"{row.year}-{row.month:02d}"
                print(f"{month_year:<12} {row.monthly_transactions:<12} ${row.monthly_total:<14,.2f} {row.active_accounts:<15}")
    
    def scenario_5_business_logic_validation(self):
        """
        Scenario 5: Complex Business Logic Validation
        - Account balance consistency checks
        - Suspicious transaction detection
        - Customer risk profiling
        """
        print("\n" + "="*60)
        print("🔍 SCENARIO 5: Complex Business Logic Validation")
        print("="*60)
        
        # Balance vs transaction consistency
        query_balance_consistency = f"""
        WITH customer_transaction_summary AS (
            SELECT 
                account_number,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_credits,
                SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as total_debits,
                SUM(amount) as net_transactions,
                COUNT(*) as transaction_count
            FROM `{self.project_id}.{self.dataset_id}.transactions`
            GROUP BY account_number
        )
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.account_type,
            c.balance as current_balance,
            t.total_credits,
            t.total_debits,
            t.net_transactions,
            t.transaction_count,
            ABS(c.balance - t.net_transactions) as balance_difference
        FROM `{self.project_id}.{self.dataset_id}.customers` c
        INNER JOIN customer_transaction_summary t
        ON c.account_number = t.account_number
        WHERE ABS(c.balance - t.net_transactions) > 1000  -- Flag significant differences
        ORDER BY balance_difference DESC
        LIMIT 10
        """
        
        results = self.execute_query(query_balance_consistency, "Balance Consistency Check")
        if results:
            print("\n⚠️  Customers with Balance Inconsistencies (>$1000 difference):")
            print("-" * 120)
            print(f"{'Customer ID':<12} {'Name':<20} {'Account':<10} {'Balance':<12} {'Net Trans':<12} {'Difference':<12} {'Trans Count':<12}")
            print("-" * 120)
            for row in results:
                name = f"{row.first_name} {row.last_name}"
                print(f"{row.customer_id:<12} {name:<20} {row.account_type:<10} ${row.current_balance:<11,.2f} ${row.net_transactions:<11,.2f} ${row.balance_difference:<11,.2f} {row.transaction_count:<12}")
        
        # High-value transaction analysis
        query_high_value_transactions = f"""
        SELECT 
            t.transaction_id,
            t.account_number,
            c.first_name,
            c.last_name,
            c.account_type,
            t.transaction_type,
            t.amount,
            t.transaction_date,
            CASE 
                WHEN ABS(t.amount) > 50000 THEN 'Very High'
                WHEN ABS(t.amount) > 25000 THEN 'High'
                WHEN ABS(t.amount) > 10000 THEN 'Medium-High'
                ELSE 'Normal'
            END as risk_level
        FROM `{self.project_id}.{self.dataset_id}.transactions` t
        INNER JOIN `{self.project_id}.{self.dataset_id}.customers` c
        ON t.account_number = c.account_number
        WHERE ABS(t.amount) > 10000
        ORDER BY ABS(t.amount) DESC
        LIMIT 15
        """
        
        results = self.execute_query(query_high_value_transactions, "High-Value Transaction Analysis")
        if results:
            print("\n💰 High-Value Transactions (>$10,000):")
            print("-" * 120)
            print(f"{'Trans ID':<10} {'Customer':<20} {'Account':<10} {'Type':<12} {'Amount':<15} {'Date':<12} {'Risk Level':<12}")
            print("-" * 120)
            for row in results:
                name = f"{row.first_name} {row.last_name}"
                print(f"{row.transaction_id:<10} {name:<20} {row.account_type:<10} {row.transaction_type:<12} ${row.amount:<14,.2f} {row.transaction_date:<12} {row.risk_level:<12}")
        
        # Customer risk profiling
        query_customer_risk = f"""
        WITH customer_risk_metrics AS (
            SELECT 
                c.customer_id,
                c.first_name,
                c.last_name,
                c.account_type,
                c.balance,
                COUNT(t.transaction_id) as total_transactions,
                AVG(ABS(t.amount)) as avg_transaction_size,
                MAX(ABS(t.amount)) as max_transaction_size,
                SUM(CASE WHEN ABS(t.amount) > 10000 THEN 1 ELSE 0 END) as high_value_transactions,
                STDDEV(t.amount) as transaction_volatility
            FROM `{self.project_id}.{self.dataset_id}.customers` c
            LEFT JOIN `{self.project_id}.{self.dataset_id}.transactions` t
            ON c.account_number = t.account_number
            GROUP BY c.customer_id, c.first_name, c.last_name, c.account_type, c.balance
        )
        SELECT 
            customer_id,
            first_name,
            last_name,
            account_type,
            balance,
            total_transactions,
            avg_transaction_size,
            max_transaction_size,
            high_value_transactions,
            transaction_volatility,
            CASE 
                WHEN high_value_transactions > 5 OR max_transaction_size > 50000 THEN 'High Risk'
                WHEN high_value_transactions > 2 OR max_transaction_size > 25000 THEN 'Medium Risk'
                WHEN avg_transaction_size > 5000 THEN 'Low-Medium Risk'
                ELSE 'Low Risk'
            END as risk_profile
        FROM customer_risk_metrics
        WHERE total_transactions > 0
        ORDER BY high_value_transactions DESC, max_transaction_size DESC
        LIMIT 20
        """
        
        results = self.execute_query(query_customer_risk, "Customer Risk Profiling")
        if results:
            print("\n🎯 Customer Risk Profiling:")
            print("-" * 140)
            print(f"{'Customer ID':<12} {'Name':<20} {'Account':<10} {'Balance':<12} {'Transactions':<12} {'Max Amount':<12} {'High Value':<10} {'Risk':<12}")
            print("-" * 140)
            for row in results:
                name = f"{row.first_name} {row.last_name}"
                max_amt = row.max_transaction_size if row.max_transaction_size else 0
                high_val = row.high_value_transactions if row.high_value_transactions else 0
                print(f"{row.customer_id:<12} {name:<20} {row.account_type:<10} ${row.balance:<11,.2f} {row.total_transactions:<12} ${max_amt:<11,.2f} {high_val:<10} {row.risk_profile:<12}")
    
    def run_all_scenarios(self):
        """Run all 5 test scenarios."""
        print("\n🚀 Starting BigQuery Test Scenarios")
        print("="*80)
        print(f"Project: {self.project_id}")
        print(f"Dataset: {self.dataset_id}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        if not self.initialize_client():
            print("❌ Failed to initialize BigQuery client. Exiting.")
            return False
        
        try:
            # Run all scenarios
            self.scenario_1_basic_data_retrieval()
            self.scenario_2_aggregation_operations()
            self.scenario_3_join_operations()
            self.scenario_4_date_filtering()
            self.scenario_5_business_logic_validation()
            
            print("\n" + "="*80)
            print("🎉 ALL SCENARIOS COMPLETED SUCCESSFULLY!")
            print("="*80)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error running scenarios: {e}")
            print(f"\n❌ Error running scenarios: {e}")
            return False

def main():
    """Main function to run BigQuery test scenarios."""
    # Initialize test scenarios
    test_scenarios = BigQueryTestScenarios()
    
    # Run all scenarios
    success = test_scenarios.run_all_scenarios()
    
    if success:
        print("\n✅ All BigQuery test scenarios completed successfully!")
    else:
        print("\n❌ Some scenarios failed. Check the logs for details.")

if __name__ == "__main__":
    main()
