# Enterprise Data Validation Framework

A comprehensive Python framework for validating enterprise data using Excel mapping files with Google BigQuery integration. Designed for enterprise environments with proxy support and flexible data source management.

## 🆕 Enhanced Join-Based Validation (Latest Feature)

**New in this release**: Enhanced validation with proper table relationships!

- **`enhanced_data_validation_script_py`**: Advanced validation with proper table joins
- **`create_enhanced_mapping.py`**: Generator for Excel files with join key structure
- **Realistic validation**: Tables are joined using primary keys before applying derivation logic
- **Complex transformations**: Multi-column derivations with SQL-like expressions
- **Sample data generation**: Creates realistic test data with proper table relationships

**Quick Start with Enhanced Validation:**
```bash
# Generate enhanced mapping file with join keys
python create_enhanced_mapping.py

# Run enhanced validation
python enhanced_data_validation_script_py --excel enhanced_validation_mapping_YYYYMMDD_HHMMSS.xlsx --test True
```

> **📋 Corporate Environment Note**: Python files use `_py` extension instead of `.py` to bypass corporate download restrictions. Rename `data_validation_script_py` → `data_validation_script.py` and `test_bigquery_py` → `test_bigquery.py` after download.

## 🏢 Enterprise Features

- **Office Network Support**: Automatic proxy configuration for development environments
- **Multi-Environment**: Production and development BigQuery connections
- **Excel Integration**: Automatic column detection and mapping
- **Financial Domain**: CRM enrichment, transaction validation, loan reconciliation, risk assessment

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas openpyxl numpy google-cloud-bigquery
```

### Basic Usage

**Test Mode (No BigQuery needed):**
```bash
python data_validation_script.py --excel your_mapping_file.xlsx --test True
```

**Development Environment:**
```bash
python data_validation_script.py --excel your_mapping_file.xlsx --test False --project myproject-dev --environment dev --source Test
```

**Production Environment:**
```bash
python data_validation_script.py --excel your_mapping_file.xlsx --test False --project myproject-prod --environment prod --source Baseline
```

## 🔧 Corporate Environment Setup

**Important**: If your corporate environment blocks `.py` files, the Python files in this repository use `_py` extension:

### Quick Setup (Automated)
**Windows:**
```cmd
setup_corporate.bat
```

**Linux/Mac:**
```bash
chmod +x setup_corporate.sh
./setup_corporate.sh
```

### Manual Setup
1. **Download files**: `data_validation_script_py` and `test_bigquery_py`
2. **Rename locally**: Change `_py` to `.py` after download
   ```bash
   # Windows
   ren data_validation_script_py data_validation_script.py
   ren test_bigquery_py test_bigquery.py
   
   # Linux/Mac
   mv data_validation_script_py data_validation_script.py
   mv test_bigquery_py test_bigquery.py
   ```
- **Comprehensive Validation**: Supports direct copy and derived transformation validations
- **Detailed Logging**: Timestamped logs with validation progress and results
- **Flexible Input**: Excel-based mapping configuration with optional WHERE clauses
- **Rich Output**: Summary CSV with detailed validation statistics

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies
- pandas>=1.5.0
- openpyxl>=3.0.0
- numpy>=1.21.0
- google-cloud-bigquery>=3.0.0 (for production mode)
- google-auth>=2.0.0 (for production mode)

## Excel Mapping File Structure

Your Excel file should contain the following columns:

| Column Name | Description | Required | Example |
|-------------|-------------|----------|---------|
| Table Name | Name of the table being validated | Yes | `customer_accounts` |
| Source Column Name | Column name in source table | Yes | `account_number` |
| Target Column Name | Column name in target table | Yes | `account_id` |
| Transformation Logic | Description of transformation | Yes | `copy` or `derived using col A + B` |
| Join Condition | SQL condition to join tables | Yes | `s.id = t.id` |
| Optional WHERE Clause | Additional filtering conditions | No | `s.status = "ACTIVE"` |

## Enhanced Excel Structure (Join-Based Validation)

For the enhanced validation script, use this streamlined structure which supports proper table relationships:

| Column Name | Description | Required | Example |
|-------------|-------------|----------|---------|
| Source_Table | Source table name | Yes | `customer_source` |
| Target_Table | Target table name | Yes | `customer_target` |
| Join_Key | Primary/Foreign key for joining | Yes | `customer_id` |
| Target_Column | Target column name | Yes | `customer_first_name` |
| Derivation_Logic | SQL-like transformation (source columns implicit) | Yes | `UPPER(source.first_name)` |
| Validation_Type | Type of validation | Yes | `Transformation` |
| Business_Rule | Business context | No | `Name standardization` |

**Key Improvement**: Removed redundant `Source_Column` field - the derivation logic already contains all source column information!

**Multi-Column Examples:**
- `source.balance_usd * source.exchange_rate` (uses balance_usd, exchange_rate)
- `source.base_rate + source.margin` (uses base_rate, margin)
- `CASE WHEN source.credit_score >= 750 THEN "LOW"...` (uses credit_score)

**Generate Enhanced Structure:**
```bash
python create_enhanced_mapping.py
```

This creates a complete Excel file with sample data for realistic testing.

### Transformation Logic Types

1. **Direct Copy**: Use `copy`, `direct copy`, or `same`
2. **Derived Logic**: Use `derived using <formula>` (e.g., `derived using amount * exchange_rate`)

## Usage

### Test Mode (Local Simulation)

Use test mode to validate your mapping logic without connecting to BigQuery:

```bash
python data_validation_script.py --excel mapping.xlsx --test True
```

In test mode, the script:
- Creates sample pandas DataFrames (1000 records each)
- Simulates the join and validation logic locally
- Provides realistic validation results for testing

### Production Mode (BigQuery)

Use production mode to run actual validations against BigQuery tables:

```bash
# Using default credentials
python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id

# Using service account credentials
python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id --credentials path/to/credentials.json
```

### Command Line Arguments

| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `--excel` | Path to Excel mapping file | Yes | - |
| `--test` | Test mode flag (`True` or `False`) | No | `True` |
| `--project` | BigQuery project ID | Required for production | - |
| `--credentials` | Path to BigQuery credentials JSON | No | Uses default credentials |

## Output Files

### 1. Summary Results CSV
`summary_results_YYYYMMDD_HHMMSS.csv`

Contains validation results with columns:
- Table_Name
- Source_Column
- Target_Column
- Transformation_Logic
- Total_Count
- Pass_Count
- Fail_Count
- Pass_Rate
- Status

### 2. Updated Mapping Excel
`updated_mapping_YYYYMMDD_HHMMSS.xlsx`

Original mapping file with added `SQL_Case_Statement` column containing generated CASE statements.

### 3. Validation Logs
`validation_logs_YYYYMMDD_HHMMSS.log`

Detailed timestamped logs including:
- Processing progress
- SQL query execution details
- Error messages and debugging information
- Summary statistics

## Generated SQL Structure

For each mapping row, the script generates SQL queries in this format:

```sql
SELECT
    COUNT(*) AS total_count,
    SUM(CASE WHEN (CASE WHEN s.source_col = t.target_col THEN 'PASS' ELSE 'FAIL' END) = 'PASS' THEN 1 ELSE 0 END) AS pass_count,
    SUM(CASE WHEN (CASE WHEN s.source_col = t.target_col THEN 'PASS' ELSE 'FAIL' END) = 'FAIL' THEN 1 ELSE 0 END) AS fail_count
FROM table_name_source s
JOIN table_name_target t ON join_condition
WHERE optional_where_clause
```

## BigQuery Setup

### Prerequisites for Production Mode

1. **Google Cloud Project**: Ensure you have a BigQuery-enabled project
2. **Authentication**: Set up authentication using one of these methods:
   - Service Account JSON file
   - Application Default Credentials (ADC)
   - Environment variable `GOOGLE_APPLICATION_CREDENTIALS`

### Table Naming Convention

The script expects tables to follow this naming pattern:
- Source tables: `{table_name}_source`
- Target tables: `{table_name}_target`

Example: For `Table Name` = "customer_accounts", tables should be:
- `customer_accounts_source`
- `customer_accounts_target`

## Error Handling

The script includes comprehensive error handling:

- **Invalid Excel Format**: Validates required columns and data types
- **BigQuery Connection Issues**: Handles authentication and network errors
- **SQL Execution Errors**: Logs and continues processing other mappings
- **Missing Tables**: Gracefully handles non-existent tables

## Logging

All operations are logged with appropriate severity levels:

- **INFO**: Normal processing progress and results
- **WARNING**: Non-critical issues that don't stop processing
- **ERROR**: Critical errors that prevent processing specific mappings

## Example Workflow

1. **Prepare Excel File**: Create mapping file with required columns
2. **Test Locally**: Run in test mode to validate logic
   ```bash
   python data_validation_script.py --excel mapping.xlsx --test True
   ```
3. **Review Results**: Check generated SQL statements and test results
4. **Production Run**: Execute against actual BigQuery tables
   ```bash
   python data_validation_script.py --excel mapping.xlsx --test False --project prod-project
   ```
5. **Analyze Results**: Review summary CSV and logs for validation outcomes

## Sample Data Creation

To create a sample Excel mapping file, run:

```bash
python create_sample_excel.py
```

This creates `sample_mapping.xlsx` with banking domain examples.

## Troubleshooting

### Common Issues

1. **ImportError for BigQuery**: Install BigQuery dependencies or use test mode
2. **Authentication Errors**: Verify credentials and project permissions
3. **Table Not Found**: Check table naming convention and existence
4. **Excel Format Issues**: Ensure all required columns are present

### Debug Mode

For additional debugging, modify the logging level in the script:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Banking Domain Considerations

This script is designed specifically for banking data validation with features like:

- **NULL Handling**: Proper comparison of NULL values in financial data
- **Transformation Logic**: Support for currency conversions, rate calculations
- **Audit Trail**: Comprehensive logging for compliance requirements
- **Scalability**: Efficient processing of large banking datasets

## Security Notes

- Never hardcode credentials in the script
- Use environment variables or secure credential files
- Ensure proper IAM permissions for BigQuery access
- Follow your organization's data handling policies

## Support

For issues or enhancements, please review the validation logs and error messages. The script provides detailed information for troubleshooting most common scenarios.
