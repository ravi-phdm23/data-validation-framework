#!/usr/bin/env python3
"""
Sample Data Generator for BigQuery Upload Test
Creates realistic banking/financial data for testing data validation scenarios
Project ID: cohesive-apogee-411113
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

def generate_customer_data(num_records=1000):
    """Generate sample customer data."""
    
    # Set random seed for reproducible data
    np.random.seed(42)
    random.seed(42)
    
    # Sample data lists
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'William', 'Jennifer',
                   'James', 'Mary', 'Christopher', 'Patricia', 'Daniel', 'Linda', 'Matthew', 'Elizabeth', 'Anthony', 'Barbara']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
              'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'Seattle', 'Denver', 'Boston']
    
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'WA', 'CO', 'MA', 'NC', 'OH']
    
    account_types = ['CHECKING', 'SAVINGS', 'CREDIT', 'INVESTMENT', 'LOAN']
    
    # Generate data
    data = []
    
    for i in range(num_records):
        customer_id = f"CUST_{i+1:06d}"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Account information
        account_number = f"ACC_{random.randint(100000000, 999999999)}"
        account_type = random.choice(account_types)
        
        # Financial data
        if account_type == 'CHECKING':
            balance = round(random.uniform(100, 50000), 2)
        elif account_type == 'SAVINGS':
            balance = round(random.uniform(500, 100000), 2)
        elif account_type == 'CREDIT':
            balance = round(random.uniform(-10000, 0), 2)  # Negative for credit
        elif account_type == 'INVESTMENT':
            balance = round(random.uniform(1000, 500000), 2)
        else:  # LOAN
            balance = round(random.uniform(-100000, -1000), 2)  # Negative for loans
        
        # Date fields
        account_open_date = datetime.now() - timedelta(days=random.randint(30, 3650))
        last_transaction_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # Address
        address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'First', 'Second'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr'])}"
        city = random.choice(cities)
        state = random.choice(states)
        zip_code = f"{random.randint(10000, 99999)}"
        
        # Risk and status fields
        risk_score = random.randint(300, 850)  # Credit score like
        account_status = random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'DORMANT', 'CLOSED'])  # More active accounts
        
        # Monthly income (for some customers)
        monthly_income = round(random.uniform(3000, 15000), 2) if random.random() > 0.1 else None
        
        data.append({
            'customer_id': customer_id,
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}",
            'account_number': account_number,
            'account_type': account_type,
            'balance': balance,
            'account_open_date': account_open_date.strftime('%Y-%m-%d'),
            'last_transaction_date': last_transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'risk_score': risk_score,
            'account_status': account_status,
            'monthly_income': monthly_income,
            'created_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(data)

def generate_transaction_data(num_records=5000):
    """Generate sample transaction data."""
    
    np.random.seed(42)
    random.seed(42)
    
    transaction_types = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT', 'FEE', 'INTEREST']
    channels = ['ATM', 'ONLINE', 'MOBILE', 'BRANCH', 'PHONE']
    merchants = ['Amazon', 'Walmart', 'Target', 'Starbucks', 'Shell', 'McDonald\'s', 'Uber', 'Netflix', 'Spotify', 'Apple']
    
    data = []
    
    for i in range(num_records):
        transaction_id = f"TXN_{i+1:08d}"
        account_number = f"ACC_{random.randint(100000000, 999999999)}"
        
        transaction_type = random.choice(transaction_types)
        
        # Amount based on transaction type
        if transaction_type == 'DEPOSIT':
            amount = round(random.uniform(100, 5000), 2)
        elif transaction_type == 'WITHDRAWAL':
            amount = round(random.uniform(-500, -10), 2)
        elif transaction_type == 'TRANSFER':
            amount = round(random.uniform(-2000, 2000), 2)
        elif transaction_type == 'PAYMENT':
            amount = round(random.uniform(-1000, -5), 2)
        elif transaction_type == 'FEE':
            amount = round(random.uniform(-50, -2.5), 2)
        else:  # INTEREST
            amount = round(random.uniform(0.5, 100), 2)
        
        # Transaction details
        transaction_date = datetime.now() - timedelta(days=random.randint(0, 90))
        channel = random.choice(channels)
        merchant = random.choice(merchants) if transaction_type in ['PAYMENT', 'WITHDRAWAL'] else None
        
        # Location
        transaction_city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
        transaction_state = random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'])
        
        # Status and flags
        status = random.choice(['COMPLETED', 'COMPLETED', 'COMPLETED', 'PENDING', 'FAILED'])
        is_fraudulent = random.choice([True, False, False, False, False])  # 20% fraud rate
        
        data.append({
            'transaction_id': transaction_id,
            'account_number': account_number,
            'transaction_type': transaction_type,
            'amount': amount,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'transaction_timestamp': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'channel': channel,
            'merchant': merchant,
            'transaction_city': transaction_city,
            'transaction_state': transaction_state,
            'status': status,
            'is_fraudulent': is_fraudulent,
            'processing_fee': round(random.uniform(0, 3.5), 2) if transaction_type != 'DEPOSIT' else 0,
            'created_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return pd.DataFrame(data)

def create_sample_files():
    """Create all sample data files."""
    
    print("🏦 Generating Banking Sample Data for BigQuery Upload")
    print("=" * 60)
    
    # Generate customer data
    print("📊 Generating customer data (1000 records)...")
    customers_df = generate_customer_data(1000)
    
    # Generate transaction data
    print("💳 Generating transaction data (5000 records)...")
    transactions_df = generate_transaction_data(5000)
    
    # Save to CSV files
    customer_file = "sample_customers.csv"
    transaction_file = "sample_transactions.csv"
    
    print(f"💾 Saving customer data to: {customer_file}")
    customers_df.to_csv(customer_file, index=False)
    
    print(f"💾 Saving transaction data to: {transaction_file}")
    transactions_df.to_csv(transaction_file, index=False)
    
    # Create BigQuery schema files
    print("📝 Creating BigQuery schema files...")
    
    # Customer schema
    customer_schema = [
        {"name": "customer_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "first_name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "last_name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "account_number", "type": "STRING", "mode": "REQUIRED"},
        {"name": "account_type", "type": "STRING", "mode": "REQUIRED"},
        {"name": "balance", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "account_open_date", "type": "DATE", "mode": "REQUIRED"},
        {"name": "last_transaction_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "address", "type": "STRING", "mode": "REQUIRED"},
        {"name": "city", "type": "STRING", "mode": "REQUIRED"},
        {"name": "state", "type": "STRING", "mode": "REQUIRED"},
        {"name": "zip_code", "type": "STRING", "mode": "REQUIRED"},
        {"name": "risk_score", "type": "INTEGER", "mode": "REQUIRED"},
        {"name": "account_status", "type": "STRING", "mode": "REQUIRED"},
        {"name": "monthly_income", "type": "FLOAT64", "mode": "NULLABLE"},
        {"name": "created_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"}
    ]
    
    # Transaction schema
    transaction_schema = [
        {"name": "transaction_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "account_number", "type": "STRING", "mode": "REQUIRED"},
        {"name": "transaction_type", "type": "STRING", "mode": "REQUIRED"},
        {"name": "amount", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "transaction_date", "type": "DATE", "mode": "REQUIRED"},
        {"name": "transaction_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
        {"name": "channel", "type": "STRING", "mode": "REQUIRED"},
        {"name": "merchant", "type": "STRING", "mode": "NULLABLE"},
        {"name": "transaction_city", "type": "STRING", "mode": "REQUIRED"},
        {"name": "transaction_state", "type": "STRING", "mode": "REQUIRED"},
        {"name": "status", "type": "STRING", "mode": "REQUIRED"},
        {"name": "is_fraudulent", "type": "BOOLEAN", "mode": "REQUIRED"},
        {"name": "processing_fee", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "created_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"}
    ]
    
    # Save schema files
    with open("customer_schema.json", "w") as f:
        json.dump(customer_schema, f, indent=2)
    
    with open("transaction_schema.json", "w") as f:
        json.dump(transaction_schema, f, indent=2)
    
    print("✅ Schema files created: customer_schema.json, transaction_schema.json")
    
    # Display sample data
    print("\n📋 Sample Customer Data (first 5 rows):")
    print(customers_df.head().to_string())
    
    print("\n📋 Sample Transaction Data (first 5 rows):")
    print(transactions_df.head().to_string())
    
    print(f"\n📈 Data Summary:")
    print(f"   • Customers: {len(customers_df):,} records")
    print(f"   • Transactions: {len(transactions_df):,} records")
    print(f"   • Customer file size: {customers_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    print(f"   • Transaction file size: {transactions_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    return customer_file, transaction_file

def create_bigquery_upload_script():
    """Create a script to upload data to BigQuery."""
    
    upload_script = '''#!/usr/bin/env python3
"""
Upload sample data to BigQuery
Project ID: cohesive-apogee-411113
"""

from google.cloud import bigquery
import pandas as pd
import json

def upload_to_bigquery():
    """Upload sample data to BigQuery."""
    
    # Initialize BigQuery client
    client = bigquery.Client(project="cohesive-apogee-411113")
    
    # Dataset and table configuration
    dataset_id = "banking_sample_data"
    customer_table_id = "customers"
    transaction_table_id = "transactions"
    
    print(f"🏗️  Creating dataset: {dataset_id}")
    
    # Create dataset
    dataset = bigquery.Dataset(f"cohesive-apogee-411113.{dataset_id}")
    dataset.location = "US"
    
    try:
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"✅ Created dataset {dataset.dataset_id}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ Dataset {dataset_id} already exists")
        else:
            print(f"❌ Error creating dataset: {e}")
            return False
    
    # Upload customers table
    print(f"📤 Uploading customer data...")
    
    # Load customer schema
    with open("customer_schema.json", "r") as f:
        customer_schema = [bigquery.SchemaField.from_api_repr(field) for field in json.load(f)]
    
    customer_table_ref = client.dataset(dataset_id).table(customer_table_id)
    customer_table = bigquery.Table(customer_table_ref, schema=customer_schema)
    
    try:
        customer_table = client.create_table(customer_table)
        print(f"✅ Created table {customer_table_id}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ Table {customer_table_id} already exists, will replace data")
        else:
            print(f"❌ Error creating customer table: {e}")
    
    # Load and upload customer data
    customers_df = pd.read_csv("sample_customers.csv")
    
    job_config = bigquery.LoadJobConfig(
        schema=customer_schema,
        write_disposition="WRITE_TRUNCATE",  # Replace existing data
    )
    
    job = client.load_table_from_dataframe(customers_df, customer_table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete
    
    print(f"✅ Uploaded {len(customers_df)} customer records")
    
    # Upload transactions table
    print(f"📤 Uploading transaction data...")
    
    # Load transaction schema
    with open("transaction_schema.json", "r") as f:
        transaction_schema = [bigquery.SchemaField.from_api_repr(field) for field in json.load(f)]
    
    transaction_table_ref = client.dataset(dataset_id).table(transaction_table_id)
    transaction_table = bigquery.Table(transaction_table_ref, schema=transaction_schema)
    
    try:
        transaction_table = client.create_table(transaction_table)
        print(f"✅ Created table {transaction_table_id}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ Table {transaction_table_id} already exists, will replace data")
        else:
            print(f"❌ Error creating transaction table: {e}")
    
    # Load and upload transaction data
    transactions_df = pd.read_csv("sample_transactions.csv")
    
    job_config = bigquery.LoadJobConfig(
        schema=transaction_schema,
        write_disposition="WRITE_TRUNCATE",  # Replace existing data
    )
    
    job = client.load_table_from_dataframe(transactions_df, transaction_table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete
    
    print(f"✅ Uploaded {len(transactions_df)} transaction records")
    
    # Test queries
    print(f"\\n🧪 Testing uploaded data...")
    
    # Test customer data
    query = f"""
    SELECT 
        account_type,
        COUNT(*) as count,
        AVG(balance) as avg_balance,
        MIN(account_open_date) as earliest_account,
        MAX(account_open_date) as latest_account
    FROM `cohesive-apogee-411113.{dataset_id}.{customer_table_id}`
    GROUP BY account_type
    ORDER BY count DESC
    """
    
    print("Customer data summary:")
    query_job = client.query(query)
    results = query_job.result()
    
    for row in results:
        print(f"  {row.account_type}: {row.count} accounts, avg balance: ${row.avg_balance:.2f}")
    
    # Test transaction data
    query = f"""
    SELECT 
        transaction_type,
        COUNT(*) as count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM `cohesive-apogee-411113.{dataset_id}.{transaction_table_id}`
    GROUP BY transaction_type
    ORDER BY count DESC
    """
    
    print("\\nTransaction data summary:")
    query_job = client.query(query)
    results = query_job.result()
    
    for row in results:
        print(f"  {row.transaction_type}: {row.count} transactions, total: ${row.total_amount:.2f}")
    
    print(f"\\n🎉 Data upload completed successfully!")
    print(f"\\n📋 Your BigQuery tables:")
    print(f"   • cohesive-apogee-411113.{dataset_id}.{customer_table_id}")
    print(f"   • cohesive-apogee-411113.{dataset_id}.{transaction_table_id}")
    
    return True

if __name__ == "__main__":
    upload_to_bigquery()
'''
    
    with open("upload_to_bigquery.py", "w") as f:
        f.write(upload_script)
    
    print("📝 Created BigQuery upload script: upload_to_bigquery.py")

if __name__ == "__main__":
    print("🚀 Starting sample data generation...")
    
    # Generate sample files
    customer_file, transaction_file = create_sample_files()
    
    # Create upload script
    create_bigquery_upload_script()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("=" * 60)
    print("1. Ensure you're authenticated with Google Cloud:")
    print("   gcloud auth application-default login")
    print("2. Upload the data to BigQuery:")
    print("   python upload_to_bigquery.py")
    print("3. Test your production scenario with real data!")
    print()
    print("💡 Files created:")
    print(f"   • {customer_file} - Customer data (1000 records)")
    print(f"   • {transaction_file} - Transaction data (5000 records)")
    print("   • customer_schema.json - BigQuery schema for customers")
    print("   • transaction_schema.json - BigQuery schema for transactions")
    print("   • upload_to_bigquery.py - Script to upload data to BigQuery")
    print()
    print("🏦 This creates a realistic banking dataset for testing your")
    print("    data validation framework with production-like scenarios!")
