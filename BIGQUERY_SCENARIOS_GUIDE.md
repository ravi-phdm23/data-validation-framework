# BigQuery Test Scenarios - Quick Reference Guide

## Overview
This document describes 5 simple BigQuery testing scenarios designed to validate different aspects of BigQuery functionality using real banking data.

**Project**: cohesive-apogee-411113  
**Dataset**: banking_sample_data  
**Tables**: customers (1000 records), transactions (5000 records)

---

## Scenario 1: Basic Data Retrieval and Counting
**Purpose**: Test fundamental BigQuery operations  
**What it tests**:
- COUNT operations
- DISTINCT operations
- MIN/MAX date functions
- Basic table querying

**Expected Results**:
- Total customer count: ~1000
- Total transaction count: ~5000
- Date range of transactions
- Number of unique account/transaction types

**Key SQL Features**:
```sql
SELECT COUNT(*), COUNT(DISTINCT column_name), MIN(date), MAX(date)
```

---

## Scenario 2: Aggregation and Grouping Operations
**Purpose**: Test BigQuery's aggregation capabilities  
**What it tests**:
- GROUP BY operations
- SUM, AVG, MIN, MAX functions
- ORDER BY operations
- Multiple aggregations in single query

**Expected Results**:
- Transaction summaries by type (DEPOSIT, WITHDRAWAL, TRANSFER, etc.)
- Account balance statistics by account type (CHECKING, SAVINGS, etc.)
- Financial totals and averages

**Key SQL Features**:
```sql
SELECT column, COUNT(*), SUM(amount), AVG(amount)
FROM table
GROUP BY column
ORDER BY SUM(amount) DESC
```

---

## Scenario 3: Join Operations Between Tables
**Purpose**: Test BigQuery's JOIN capabilities  
**What it tests**:
- LEFT JOIN operations
- INNER JOIN operations
- Cross-table data correlation
- Customer-transaction relationships

**Expected Results**:
- Top 10 most active customers with transaction counts
- Transaction patterns by account type
- Customer activity analysis combining both tables

**Key SQL Features**:
```sql
SELECT c.*, t.*
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id
```

---

## Scenario 4: Date Filtering and Range Queries
**Purpose**: Test BigQuery's date/time functions  
**What it tests**:
- DATE_SUB operations
- EXTRACT functions for year/month
- Date range filtering
- Time-based aggregations

**Expected Results**:
- Recent transactions (last 30 days)
- Monthly transaction trends
- Daily transaction summaries
- Active customer counts by month

**Key SQL Features**:
```sql
WHERE date >= DATE_SUB(MAX(date), INTERVAL 30 DAY)
EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
```

---

## Scenario 5: Complex Business Logic Validation
**Purpose**: Test advanced BigQuery analytical capabilities  
**What it tests**:
- Common Table Expressions (CTEs)
- CASE statements for business rules
- Complex calculations and validations
- Data quality checks

**Expected Results**:
- Balance consistency checks (finding discrepancies)
- High-value transaction detection (>$10,000)
- Customer risk profiling based on transaction patterns
- Suspicious activity identification

**Key SQL Features**:
```sql
WITH cte AS (SELECT ...), 
CASE WHEN condition THEN 'value' ELSE 'other' END,
ABS(amount), STDDEV(amount)
```

---

## How to Run

### Option 1: Run All Scenarios
```bash
python bigquery_test_scenarios.py
```

### Option 2: Run Individual Scenarios (modify the script)
Comment out scenarios in the `run_all_scenarios()` method to run specific tests.

---

## Expected Output Format

Each scenario provides:
1. **Scenario Header**: Clear identification of what's being tested
2. **Query Execution Log**: SQL query being executed
3. **Formatted Results**: Tables with aligned columns showing data
4. **Success/Error Messages**: Clear indication of test status

---

## Troubleshooting

### Common Issues:
1. **Authentication Error**: Run `gcloud auth application-default login`
2. **Project Not Found**: Verify project ID is correct
3. **Dataset/Table Not Found**: Ensure data was uploaded successfully
4. **Permission Denied**: Check BigQuery API is enabled

### Verification Commands:
```bash
# Check authentication
gcloud auth list

# Verify project access
gcloud config get-value project

# Test basic BigQuery access
python test_shakespeare_query.py
```

---

## Sample Expected Results

### Scenario 1 Output:
```
📈 Total Customers: 1000
📈 Unique Account Types: 4
📈 Total Transactions: 5000
📅 Date Range: 2024-01-01 to 2024-12-31
```

### Scenario 2 Output:
```
📊 Transaction Summary by Type:
Type         Count    Total Amount    Avg Amount   
DEPOSIT      1250     $1,250,000.00   $1,000.00    
WITHDRAWAL   1200     $-600,000.00    $-500.00     
```

### Scenario 3 Output:
```
👥 Top 10 Most Active Customers:
Customer ID  Name                 Account Type  Transactions
CUST_001     John Smith          CHECKING      15          
CUST_002     Jane Doe            SAVINGS       12          
```

---

## Performance Notes

- **Query Execution Time**: Should be under 10 seconds per scenario
- **Data Volume**: Testing with 1K customers, 5K transactions (small dataset)
- **Scalability**: These queries can handle much larger datasets
- **Cost**: Minimal cost due to small data size

---

## Next Steps

After running these scenarios successfully:
1. Scale up to larger datasets
2. Add more complex business rules
3. Implement data validation frameworks
4. Create automated testing pipelines
5. Add performance benchmarking
