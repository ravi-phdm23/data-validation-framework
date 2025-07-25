# BigQuery Test Scenarios - Banking Data Validation

This repository contains simple BigQuery testing scenarios using real banking data to validate different aspects of BigQuery functionality.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up authentication:**
   ```bash
   gcloud auth application-default login
   ```

3. **Option A: Use the Web Interface (Recommended)**
   ```bash
   streamlit run streamlit_app.py
   ```
   Opens an interactive web dashboard at `http://localhost:8501`

4. **Option B: Command Line Interface**
   ```bash
   # Test BigQuery connection
   python test_shakespeare_query.py
   
   # Run all 5 test scenarios
   python bigquery_test_scenarios.py
   ```

## Files Overview

### Core Scripts
- `streamlit_app.py` - **🌟 Interactive web dashboard for BigQuery testing**
- `bigquery_test_scenarios.py` - Main script with 5 BigQuery test scenarios
- `test_shakespeare_query.py` - Basic BigQuery connection test
- `generate_sample_data.py` - Generate sample banking data (1000 customers, 5000 transactions)
- `upload_csv_to_bigquery.py` - Upload CSV data to BigQuery

### Data Files
- `sample_customers.csv` - Sample customer data
- `sample_transactions.csv` - Sample transaction data

### Documentation
- `STREAMLIT_USER_GUIDE.md` - **📱 Complete guide for using the web interface**
- `BIGQUERY_SCENARIOS_GUIDE.md` - Detailed guide for all 5 test scenarios
- `requirements.txt` - Python dependencies

## 🌟 Features

### 🖥️ Interactive Web Dashboard
- **User-friendly interface** with point-and-click testing
- **Real-time results** with formatted output and visualizations
- **Custom query executor** with SQL templates and syntax highlighting
- **Data visualization** with interactive charts and graphs
- **Export functionality** for results and charts

### 📊 5 Comprehensive Test Scenarios

1. **Basic Data Retrieval and Counting** - Test fundamental BigQuery operations
2. **Aggregation and Grouping Operations** - Test BigQuery's aggregation capabilities
3. **Join Operations Between Tables** - Test BigQuery's JOIN capabilities
4. **Date Filtering and Range Queries** - Test BigQuery's date/time functions
5. **Complex Business Logic Validation** - Test advanced BigQuery analytical capabilities

## Project Details

- **Project ID**: cohesive-apogee-411113
- **Dataset**: banking_sample_data
- **Tables**: customers (1000 records), transactions (5000 records)
- **Testing Framework**: Comprehensive BigQuery functionality validation

## Sample Output

### 🖥️ Web Interface
```
🔍 BigQuery Test Scenarios Dashboard
📊 Scenario Results    🔍 Custom Queries    📈 Data Visualization    📋 Quick Stats

🟢 Connected to cohesive-apogee-411113.banking_sample_data

✅ Scenario 1: Basic Data Retrieval - Completed
✅ Scenario 2: Aggregation Operations - Completed
📈 Total Customers: 1000
📈 Total Transactions: 5000
```

### 💻 Command Line
```
🚀 Starting BigQuery Test Scenarios
📈 Total Customers: 1000
📈 Total Transactions: 5000
📊 Transaction Summary by Type:
💳 Balance Summary by Account Type:
👥 Top 10 Most Active Customers:
📅 Recent Daily Transaction Summary:
🎯 Customer Risk Profiling:
```

## Authentication

This project uses Google Cloud Application Default Credentials. Ensure you have:
1. Google Cloud CLI installed
2. Authenticated with your Google account: `gcloud auth application-default login`
3. Access to BigQuery project: cohesive-apogee-411113

## License

See LICENSE file for details.
