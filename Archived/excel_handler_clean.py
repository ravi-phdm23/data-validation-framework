#!/usr/bin/env python3
"""
Excel Handler Module - Clean Version
Enhanced Excel file processing for BigQuery validation scenarios with business logic parsing.
"""

import pandas as pd
import streamlit as st
from datetime import datetime
import logging
from typing import Dict, List, Any, Tuple, Optional
import re

# Import the SQL generator and BigQuery client
from sql_generator import (
    create_transformation_validation_sql,
    convert_business_logic_to_safe_sql,
    create_enhanced_transformation_sql,
    create_reference_table_validation_sql
)
from bigquery_client import execute_custom_query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_scenarios_from_excel(excel_data: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
    """Generate validation scenarios from Excel data with enhanced parsing."""
    scenarios = []
    
    try:
        # Look for the main scenarios sheet
        main_sheet = None
        for sheet_name, df in excel_data.items():
            if any(col in df.columns for col in ['Scenario_Name', 'Source_Table', 'Target_Table']):
                main_sheet = df
                break
        
        if main_sheet is None:
            logger.warning("No valid scenarios sheet found in Excel file")
            return scenarios
        
        # Clean column names
        main_sheet.columns = main_sheet.columns.str.strip()
        
        # Process each row as a scenario
        for index, row in main_sheet.iterrows():
            try:
                # Skip empty rows
                if pd.isna(row.get('Scenario_Name', '')) or str(row.get('Scenario_Name', '')).strip() == '':
                    continue
                
                # Extract basic scenario information
                scenario = {
                    'scenario_name': str(row.get('Scenario_Name', f'Scenario_{index+1}')).strip(),
                    'source_table': str(row.get('Source_Table', '')).strip(),
                    'target_table': str(row.get('Target_Table', '')).strip(),
                    'derivation_logic': str(row.get('Derivation_Logic', '')).strip(),
                    'validation_type': str(row.get('Validation_Type', 'Transformation')).strip(),
                    'business_rule': str(row.get('Business_Rule', '')).strip(),
                    
                    # Join keys
                    'source_join_key': str(row.get('Source_Join_Key', '')).strip(),
                    'target_join_key': str(row.get('Target_Join_Key', '')).strip(),
                    'target_column': str(row.get('Target_Column', '')).strip(),
                    
                    # Enhanced reference table support
                    'reference_table': str(row.get('Reference_Table', '')).strip(),
                    'reference_join_key': str(row.get('Reference_Join_Key', '')).strip(),
                    'reference_lookup_column': str(row.get('Reference_Lookup_Column', '')).strip(),
                    'reference_return_column': str(row.get('Reference_Return_Column', '')).strip(),
                    'business_conditions': str(row.get('Business_Conditions', '')).strip(),
                    'hardcoded_values': str(row.get('Hardcoded_Values', '')).strip(),
                    
                    # Status
                    'status': 'Ready',
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Only add if we have essential data
                if scenario['source_table'] and scenario['derivation_logic']:
                    scenarios.append(scenario)
                    logger.info(f"Generated scenario: {scenario['scenario_name']}")
                
            except Exception as e:
                logger.error(f"Error processing row {index}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error generating scenarios from Excel: {str(e)}")
        st.error(f"❌ Error processing Excel file: {str(e)}")
    
    return scenarios


def process_excel_file(uploaded_file):
    """Process uploaded Excel file and return data."""
    try:
        # Read Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        return excel_data, None
    except Exception as e:
        return None, f"❌ Error reading Excel file: {str(e)}"


def execute_all_excel_scenarios():
    """Execute all transformation validation scenarios generated from Excel."""
    if 'excel_scenarios' not in st.session_state or not st.session_state['excel_scenarios']:
        st.error("❌ No scenarios available to execute.")
        return
    
    scenarios = st.session_state['excel_scenarios']
    results = []
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, scenario in enumerate(scenarios):
        try:
            status_text.text(f"🔄 Executing scenario {i+1}/{len(scenarios)}: {scenario['scenario_name']}")
            
            # Generate SQL based on scenario type
            if scenario.get('reference_table'):
                # Reference table validation
                sql_query = create_reference_table_validation_sql(
                    source_table=f"cohesive-apogee-411113.banking_sample_data.{scenario['source_table']}",
                    target_table=f"cohesive-apogee-411113.banking_sample_data.{scenario.get('target_table', scenario['source_table'])}",
                    reference_table=f"cohesive-apogee-411113.banking_sample_data.{scenario['reference_table']}",
                    source_join_key=scenario.get('source_join_key', 'id'),
                    target_join_key=scenario.get('target_join_key', 'id'),
                    reference_join_key=scenario.get('reference_join_key', 'id'),
                    target_column=scenario['target_column'],
                    derivation_logic=scenario['derivation_logic'],
                    reference_return_column=scenario.get('reference_return_column', 'value')
                )
            elif scenario.get('target_table'):
                # Enhanced transformation validation
                sql_query = create_enhanced_transformation_sql(
                    source_table=f"cohesive-apogee-411113.banking_sample_data.{scenario['source_table']}",
                    target_table=f"cohesive-apogee-411113.banking_sample_data.{scenario['target_table']}",
                    source_join_key=scenario.get('source_join_key', 'id'),
                    target_join_key=scenario.get('target_join_key', 'id'),
                    target_column=scenario['target_column'],
                    derivation_logic=scenario['derivation_logic']
                )
            else:
                # Basic transformation validation
                sql_query = create_transformation_validation_sql(
                    source_table=f"cohesive-apogee-411113.banking_sample_data.{scenario['source_table']}",
                    derived_column_logic=scenario['derivation_logic'],
                    business_rule_description=scenario.get('business_rule', 'Validation check')
                )
            
            # Execute the query
            if sql_query:
                query_result = execute_custom_query(sql_query)
                
                if query_result is not None and not query_result.empty:
                    # Determine pass/fail based on results
                    if 'validation_result' in query_result.columns:
                        passed_count = len(query_result[query_result['validation_result'] == 'PASS'])
                        total_count = len(query_result)
                        status = 'PASS' if passed_count == total_count else 'FAIL'
                    else:
                        # If no validation_result column, check if we have any rows (failures)
                        status = 'FAIL' if len(query_result) > 0 else 'PASS'
                    
                    results.append({
                        'scenario_name': scenario['scenario_name'],
                        'status': status,
                        'total_records': len(query_result),
                        'passed_records': passed_count if 'passed_count' in locals() else 0,
                        'sql_query': sql_query,
                        'result_data': query_result,
                        'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                else:
                    results.append({
                        'scenario_name': scenario['scenario_name'],
                        'status': 'ERROR',
                        'error_message': 'No data returned from query',
                        'sql_query': sql_query,
                        'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            else:
                results.append({
                    'scenario_name': scenario['scenario_name'],
                    'status': 'ERROR',
                    'error_message': 'Failed to generate SQL query',
                    'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
        except Exception as e:
            logger.error(f"Error executing scenario {scenario['scenario_name']}: {str(e)}")
            results.append({
                'scenario_name': scenario['scenario_name'],
                'status': 'ERROR',
                'error_message': str(e),
                'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Update progress
        progress_bar.progress((i + 1) / len(scenarios))
    
    # Store results in session state
    st.session_state['scenario_results'] = results
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Show summary
    passed = len([r for r in results if r['status'] == 'PASS'])
    failed = len([r for r in results if r['status'] == 'FAIL'])
    errors = len([r for r in results if r['status'] == 'ERROR'])
    
    st.success(f"✅ Execution completed! Passed: {passed}, Failed: {failed}, Errors: {errors}")
    
    # Show results table
    if results:
        results_df = pd.DataFrame([
            {
                'Scenario': r['scenario_name'],
                'Status': r['status'],
                'Records': r.get('total_records', 0),
                'Execution Time': r['execution_time']
            }
            for r in results
        ])
        st.dataframe(results_df, use_container_width=True)


def validate_excel_format(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """Validate that the Excel file has the required format."""
    required_columns = ['Scenario_Name', 'Source_Table', 'Derivation_Logic']
    optional_columns = ['Target_Table', 'Target_Column', 'Validation_Type', 'Business_Rule']
    
    errors = []
    
    # Check for required columns
    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        errors.append(f"Missing required columns: {', '.join(missing_required)}")
    
    # Check for empty required fields
    for col in required_columns:
        if col in df.columns:
            empty_count = df[col].isna().sum() + (df[col] == '').sum()
            if empty_count > 0:
                errors.append(f"Column '{col}' has {empty_count} empty values")
    
    return len(errors) == 0, errors


def get_scenario_preview(scenarios: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a preview DataFrame of scenarios for display."""
    if not scenarios:
        return pd.DataFrame()
    
    preview_data = []
    for scenario in scenarios:
        preview_data.append({
            'Scenario Name': scenario.get('scenario_name', 'N/A'),
            'Source Table': scenario.get('source_table', 'N/A'),
            'Target Table': scenario.get('target_table', 'N/A'),
            'Validation Type': scenario.get('validation_type', 'N/A'),
            'Business Rule': scenario.get('business_rule', 'N/A')[:50] + '...' if len(scenario.get('business_rule', '')) > 50 else scenario.get('business_rule', 'N/A')
        })
    
    return pd.DataFrame(preview_data)
