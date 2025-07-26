# Streamlit BigQuery Dashboard - User Guide

## 🚀 Quick Launch

**Start the Streamlit app:**
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Features Overview

### 🔗 BigQuery Connection
- **Project ID**: Enter your Google Cloud project ID (default: cohesive-apogee-411113)
- **Dataset ID**: Enter your BigQuery dataset name (default: banking_sample_data)
- **Connect Button**: Establishes connection using your authenticated credentials

### 📊 Test Scenario Results
**5 Pre-built Test Scenarios:**
1. **Basic Data Retrieval** - Count customers, transactions, data ranges
2. **Aggregation Operations** - Transaction summaries, balance analysis
3. **Join Operations** - Customer-transaction joins, activity analysis
4. **Date Filtering** - Recent transactions, monthly trends
5. **Business Logic Validation** - Balance consistency, risk profiling

**Interactive Features:**
- Select which scenarios to run
- View real-time execution progress
- See formatted results with success/error indicators
- Expandable result sections

### 🔍 Custom Query Executor
**Query Templates:**
- Count Records
- Recent Transactions
- Top Customers by Balance
- Transaction Summary

**Features:**
- SQL syntax highlighting
- Query execution with error handling
- Results displayed in interactive tables
- Download results as CSV
- Custom query naming

### 📈 Data Visualization
**Automatic Charts:**
- Customer distribution by account type (pie chart)
- Average balance by account type (bar chart)
- Credits vs Debits by transaction type (grouped bar chart)

**Interactive Features:**
- Hover for details
- Zoom and pan
- Export charts as images

### 📋 Quick Dataset Statistics
**Real-time Metrics:**
- Total Customers
- Total Transactions
- Total Transaction Amount
- Average Customer Balance

**Recent Activity:**
- Last 10 transactions with details
- Sortable table view

## 🛠️ Technical Requirements

### Prerequisites
```bash
# Install dependencies
pip install streamlit pandas plotly google-cloud-bigquery

# Authenticate with Google Cloud
gcloud auth application-default login
```

### Data Requirements
The app expects these BigQuery tables:
- **customers**: Customer data with account information
- **transactions**: Transaction data linked to customer accounts

### Performance Notes
- **Query Execution**: Typically under 5 seconds per scenario
- **Data Volume**: Optimized for 1K+ customers, 5K+ transactions
- **Caching**: Results are cached during the session for faster re-display

## 🔧 Troubleshooting

### Connection Issues
```
❌ Not Connected
```
**Solutions:**
1. Check Google Cloud authentication: `gcloud auth list`
2. Verify project access: `gcloud config get-value project`
3. Ensure BigQuery API is enabled
4. Check project ID spelling

### Query Failures
```
❌ Query execution failed
```
**Common Causes:**
1. **Table not found**: Verify dataset and table names
2. **Permission denied**: Check BigQuery permissions
3. **SQL syntax error**: Review query syntax
4. **Data type mismatch**: Check column data types

### Performance Issues
```
⏳ Query taking too long
```
**Optimizations:**
1. Add LIMIT clauses to large queries
2. Use WHERE clauses to filter data
3. Check BigQuery slot allocation
4. Consider data partitioning

## 📱 User Interface Guide

### Sidebar Navigation
- **Configuration**: Set project and dataset
- **Connection**: Connect to BigQuery
- **Scenario Selection**: Choose tests to run

### Main Tabs
1. **📊 Scenario Results**: Pre-built test execution
2. **🔍 Custom Queries**: Free-form SQL execution
3. **📈 Data Visualization**: Charts and graphs
4. **📋 Quick Stats**: Key metrics dashboard

### Status Indicators
- 🟢 **Connected**: Ready to execute queries
- 🔴 **Not Connected**: Authentication required
- 🟡 **Not Connected**: Initial state
- ✅ **Success**: Operation completed successfully
- ❌ **Failed**: Operation encountered error
- ⚠️ **Warning**: Important information

## 🔄 Workflow Examples

### Basic Usage Flow
1. **Connect**: Enter credentials and connect to BigQuery
2. **Select**: Choose scenarios from sidebar
3. **Execute**: Click "Run Selected Scenarios"
4. **Review**: Examine results in expandable sections

### Custom Analysis Flow
1. **Template**: Choose a query template or write custom SQL
2. **Execute**: Run the query
3. **Analyze**: Review tabular results
4. **Export**: Download as CSV for further analysis

### Visualization Flow
1. **Load**: Click "Load Sample Visualizations"
2. **Explore**: Interact with charts (hover, zoom)
3. **Insights**: Analyze patterns in the data

## 💡 Best Practices

### Query Writing
- Always use LIMIT for exploratory queries
- Include comments for complex logic
- Test queries on small datasets first
- Use proper table aliases for readability

### Performance
- Run scenarios during off-peak hours for better performance
- Cache results by keeping the browser tab open
- Use specific date ranges instead of full table scans

### Data Analysis
- Compare results across different time periods
- Look for patterns in transaction types and amounts
- Validate data quality using the business logic scenarios
- Use visualizations to spot outliers and trends

## 🆘 Support

### Error Reporting
If you encounter issues:
1. Check the browser console for JavaScript errors
2. Review the terminal output for Python errors
3. Take screenshots of error messages
4. Note the exact steps to reproduce the issue

### Additional Resources
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs
- **Streamlit Documentation**: https://docs.streamlit.io
- **Plotly Documentation**: https://plotly.com/python/
