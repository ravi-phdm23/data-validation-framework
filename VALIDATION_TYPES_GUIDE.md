# 📋 VALIDATION TYPES GUIDE - BigQuery Data Validation Framework
## Complete Guide for Business Rule Validation Types

---

## 🎯 **VALIDATION TYPE CLASSIFICATION**

### **1. DIRECT_MAPPING (Column Copy)**
**Use When:** Simply copying a column value as-is with no transformation

**Examples:**
```excel
Source_Table: customers
Target_Table: customer_summary  
Source_Join_Key: customer_id
Target_Join_Key: cust_id
Target_Column: customer_name
Derivation_Logic: first_name
Validation_Type: Direct_Mapping
Business_Rule: Copy first name directly from source
```

**Generated SQL Pattern:**
```sql
SELECT 
    customer_id,
    first_name as customer_name
FROM customers
```

---

### **2. AGGREGATION**
**Use When:** Performing mathematical operations (SUM, COUNT, AVG, MIN, MAX) with GROUP BY

**Examples:**
```excel
Target_Column: total_balance
Derivation_Logic: SUM(balance) GROUP_BY customer_id
Validation_Type: Aggregation
Business_Rule: Sum all account balances per customer
```

---

### **3. TRANSFORMATION**
**Use When:** Applying business logic, calculations, or conditional statements

**Examples:**
```excel
Target_Column: risk_category
Derivation_Logic: IF(balance > 50000, "Premium", "Standard")
Validation_Type: Transformation  
Business_Rule: Categorize customers based on balance
```

---

### **4. DATA_COMPLETENESS**
**Use When:** Checking for null values, missing data, or data quality

**Examples:**
```excel
Target_Column: completeness_score
Derivation_Logic: CHECK_NOT_NULL(customer_id, first_name, address)
Validation_Type: Data_Completeness
Business_Rule: Ensure required fields are not null
```

---

### **5. FORMAT_VALIDATION**
**Use When:** Validating data formats, patterns, or structure

**Examples:**
```excel
Target_Column: address_validity
Derivation_Logic: VALIDATE_ADDRESS_FORMAT(address)
Validation_Type: Format_Validation
Business_Rule: Ensure address follows proper format
```

---

### **6. RANGE_VALIDATION**
**Use When:** Checking if values fall within acceptable ranges

**Examples:**
```excel
Target_Column: balance_status
Derivation_Logic: RANGE_CHECK(balance, min_value=0, max_value=1000000)
Validation_Type: Range_Validation
Business_Rule: Ensure balance is within valid range
```

---

### **7. CONCATENATION**
**Use When:** Combining multiple columns into one

**Examples:**
```excel
Target_Column: full_name
Derivation_Logic: CONCAT(first_name, " ", last_name)
Validation_Type: Concatenation
Business_Rule: Combine first and last name with space
```

---

### **8. DATE_TRANSFORMATION**
**Use When:** Converting or formatting date fields

**Examples:**
```excel
Target_Column: transaction_month
Derivation_Logic: FORMAT_DATE("%Y-%m", transaction_date)
Validation_Type: Date_Transformation
Business_Rule: Extract year-month from transaction date
```

---

## 🔧 **SPECIFIC EXAMPLES FOR DIRECT MAPPING**

### **Example 1: Simple Column Copy**
```excel
Scenario_Name: Copy_Customer_ID
Source_Table: customers
Target_Table: customer_profiles
Source_Join_Key: customer_id
Target_Join_Key: profile_id
Target_Column: original_customer_id
Derivation_Logic: customer_id
Validation_Type: Direct_Mapping
Business_Rule: Copy customer ID as-is to profile table
```

### **Example 2: Copy with Different Column Name**
```excel
Scenario_Name: Copy_Account_Number
Source_Table: customers
Target_Table: account_summary
Source_Join_Key: customer_id
Target_Join_Key: customer_id
Target_Column: account_ref
Derivation_Logic: account_number
Validation_Type: Direct_Mapping
Business_Rule: Copy account number to reference field
```

### **Example 3: Copy Numeric Value As-Is**
```excel
Scenario_Name: Copy_Balance
Source_Table: customers
Target_Table: balance_snapshot
Source_Join_Key: customer_id
Target_Join_Key: customer_id
Target_Column: current_balance
Derivation_Logic: balance
Validation_Type: Direct_Mapping
Business_Rule: Copy current balance without modification
```

---

## 📊 **VALIDATION TYPE DECISION TREE**

```
Is the column value copied exactly as-is?
├── YES → Direct_Mapping
└── NO → Continue below

Is there mathematical calculation (SUM, COUNT, AVG)?
├── YES → Aggregation
└── NO → Continue below

Is there conditional logic (IF/THEN/ELSE)?
├── YES → Transformation
└── NO → Continue below

Is there data quality checking?
├── YES → Data_Completeness
└── NO → Continue below

Is there format/pattern validation?
├── YES → Format_Validation
└── NO → Continue below

Is there range/boundary checking?
├── YES → Range_Validation
└── NO → Continue below

Are multiple columns being combined?
├── YES → Concatenation
└── NO → Date_Transformation (if date-related)
```

---

## ⚡ **SQL GENERATION FOR DIRECT MAPPING**

When you use `Validation_Type: Direct_Mapping`, the system generates:

```sql
-- Direct Mapping Validation: {target_column}
-- Source Table: {source_table}
-- Target Column: {target_column}
-- Derivation Logic: {derivation_logic}

WITH transformed_data AS (
    SELECT 
        {source_join_key},
        {derivation_logic} as calculated_{target_column}
    FROM `{project_id}.{dataset_id}.{source_table}`
),
validation_summary AS (
    SELECT 
        COUNT(*) as total_rows,
        COUNT(calculated_{target_column}) as non_null_rows,
        COUNT(*) - COUNT(calculated_{target_column}) as null_rows
    FROM transformed_data
)
SELECT 
    'PASS' as validation_status,
    total_rows as row_count,
    ROUND(100.0, 2) as percentage,
    CONCAT('Direct mapping successful: ', CAST(total_rows AS STRING), ' rows processed') as details
FROM validation_summary
```

---

## 📝 **COMPLETE SAMPLE FOR DIRECT MAPPING**

Here's a complete Excel row example for direct column copying:

| Column | Value |
|--------|-------|
| **Scenario_Name** | Copy_Customer_First_Name |
| **Source_Table** | customers |
| **Target_Table** | customer_profiles |
| **Source_Join_Key** | customer_id |
| **Target_Join_Key** | customer_id |
| **Target_Column** | profile_first_name |
| **Derivation_Logic** | first_name |
| **Validation_Type** | Direct_Mapping |
| **Business_Rule** | Copy customer first name directly to profile table |

---

## ✅ **VALIDATION RESULTS FOR DIRECT MAPPING**

Expected results when validation passes:
- **Status:** PASS
- **Details:** "Direct mapping successful: 1000 rows processed"
- **Row Count:** Total number of source records
- **Percentage:** 100.0% (for successful direct mapping)

---

## 🚨 **COMMON MISTAKES TO AVOID**

### **❌ Wrong Validation Type Usage:**
```excel
# WRONG - This is aggregation, not direct mapping
Derivation_Logic: SUM(balance)
Validation_Type: Direct_Mapping  # ❌ Should be "Aggregation"
```

### **✅ Correct Usage:**
```excel
# CORRECT - Simple column copy
Derivation_Logic: balance
Validation_Type: Direct_Mapping  # ✅ Correct for direct copy
```

---

## 🎯 **BOTTOM LINE**

### **Use Direct_Mapping when:**
- ✅ Copying column value exactly as-is
- ✅ No transformation or calculation applied
- ✅ Simple field-to-field mapping
- ✅ Just changing column names but keeping same value

### **Don't use Direct_Mapping when:**
- ❌ Any mathematical operation (SUM, COUNT, AVG)
- ❌ Conditional logic (IF statements)
- ❌ Data validation or quality checks
- ❌ Format transformations or concatenations

**🚀 For simple column copying, always use `Validation_Type: Direct_Mapping`!**
