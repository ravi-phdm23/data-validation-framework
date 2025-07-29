# BigQuery Data Validation Framework

A comprehensive, modular Streamlit web application for BigQuery data validation with enhanced reference table support, VLOOKUP operations, and business logic validation.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Cloud authentication:**
   ```bash
   gcloud auth application-default login
   ```

3. **Launch the web application:**
   ```bash
   streamlit run streamlit_app.py
   ```
   
   The application will open at `http://localhost:8501`

## 📁 Repository Structure (Modular Architecture)

```
├── streamlit_app.py              # Main Streamlit web application (UI layer)
├── bigquery_client.py            # BigQuery connection and query execution
├── sql_generator.py              # SQL generation for validation scenarios  
├── excel_handler.py              # Excel file processing and scenario generation
├── data_visualization.py         # Dashboard, charts, and data visualization
├── BigQuery_Test_Scenarios.xlsx  # Enhanced sample Excel template
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── LICENSE                       # License information
└── .gitignore                   # Git ignore rules
```

### 🏗️ Modular Components

- **`streamlit_app.py`** - Main UI interface with tabs and user interactions (280 lines, simplified from 2400+)
- **`bigquery_client.py`** - BigQuery connection management and query execution (69 lines)
- **`sql_generator.py`** - Comprehensive SQL generation with business logic parsing (400+ lines)
- **`excel_handler.py`** - Excel processing, scenario generation, and execution (320+ lines)
- **`data_visualization.py`** - Interactive dashboards, charts, and export functionality (400+ lines)

### ✨ Benefits of Modular Architecture

- **🔧 Maintainability** - Each module has a single responsibility and clear interface
- **🚀 Scalability** - Easy to extend functionality by adding new modules
- **🧪 Testability** - Individual modules can be tested independently
- **👥 Team Development** - Multiple developers can work on different modules simultaneously
- **🔄 Reusability** - Modules can be imported and reused in other projects
- **📖 Readability** - Clean separation of concerns makes code easier to understand

## ✨ Key Features

### 🖥️ Interactive Web Dashboard
- **User-friendly interface** with BigQuery connection management
- **Excel-based scenario generation** from business logic mapping
- **Real-time query execution** with results visualization
- **Reference table support** with VLOOKUP and conditional logic
- **Comprehensive validation dashboard** with pass/fail metrics

### 📊 Advanced Validation Capabilities
- **Reference Table Validation** - VLOOKUP-style operations with business conditions
- **Conditional Logic** - IF-THEN-ELSE business rules with hardcoded values
- **Multi-table Joins** - Complex join operations with composite keys
- **Data Quality Checks** - Completeness, range, and format validation
- **Business Rule Validation** - Custom logic for risk assessment and categorization

### 📈 Enhanced Excel Integration
Upload Excel files with enhanced mapping format supporting:
- Traditional validation (aggregations, data quality checks)
- Reference table lookups (interest rates, risk categories, etc.)
- Conditional business logic (customer tiers, product eligibility)
- Hardcoded value mappings for business conditions

## 🔧 Configuration

### Default BigQuery Settings
- **Project ID**: cohesive-apogee-411113
- **Dataset**: banking_sample_data
- **Required Tables**: customers, transactions + 9 reference tables

### Reference Tables Supported
- `interest_rates` - Account type to interest rate mapping
- `fee_structure` - Transaction fees by type and tier
- `risk_categories` - Risk scoring based on balance ranges
- `customer_tiers` - Customer classification (GOLD, SILVER, BRONZE)
- `product_categories` - Product eligibility matrix
- `customer_activity` - Activity level classifications
- `credit_limits` - Credit limit assignments
- `compliance_rules` - Regulatory compliance mappings
- `product_matrix` - Product feature matrix

## 📋 Excel Template Format

The enhanced Excel template supports these columns:

### Core Validation Columns
| Column | Description | Example |
|--------|-------------|---------|
| `Source_Table` | Source table name | `customers` |
| `Target_Column` | Column to validate | `risk_level` |
| `Derivation_Logic` | Business logic | `VLOOKUP(balance, risk_categories)` |

### Reference Table Columns
| Column | Description | Example |
|--------|-------------|---------|
| `Reference_Table` | Lookup table | `risk_categories` |
| `Reference_Join_Key` | Join key | `balance_range` |
| `Reference_Return_Column` | Return column | `risk_level` |
| `Business_Conditions` | IF-THEN logic | `balance > 50000 THEN Premium` |
| `Hardcoded_Values` | Static mappings | `Premium=VIP,Standard=Regular` |

## 🎯 Sample Scenarios

1. **Risk Score with Reference** - VLOOKUP customer balance against risk categories
2. **Interest Rate Calculation** - Apply rates based on account type and tier
3. **Compliance Flag Multi-Conditions** - Complex business rules with multiple conditions
4. **Product Eligibility Matrix** - Determine product eligibility based on customer profile
5. **Fee Structure Validation** - Calculate fees using reference table lookups

## 📊 Validation Dashboard

The application provides comprehensive validation metrics:
- **Scenario-level results** (PASS/FAIL status)
- **Row-level validation** (pass rows, fail rows, total rows)
- **Performance analytics** (execution time, query efficiency)
- **Exportable reports** (Excel format with detailed SQL queries)

## 🔐 Authentication Requirements

Ensure you have:
1. **Google Cloud CLI** installed
2. **Application Default Credentials** configured
3. **BigQuery access** to the specified project
4. **Read permissions** on required tables

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🆘 Support

For issues or questions:
1. Check the built-in **Getting Started Guide** in the application
2. Review the **Enhanced Excel File Format Guide** 
3. Verify BigQuery connection and table access
4. Ensure all reference tables are created in your dataset
