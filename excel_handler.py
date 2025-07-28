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

def generate_scenarios_from_excel(df: pd.DataFrame, project_id: str = None, dataset_id: str = None) -> List[Dict[str, Any]]:
    """Generate validation scenarios from Excel data with enhanced parsing."""
    scenarios = []
    
    try:
        # Use the provided DataFrame directly
        main_sheet = df
        
        if main_sheet is None or main_sheet.empty:
            logger.warning("No valid data found in Excel sheet")
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
            if scenario.get('reference_table') and str(scenario.get('reference_table')).lower() not in ['nan', 'none', '']:
                # Reference table validation
                sql_query = create_reference_table_validation_sql(
                    source_table=scenario['source_table'],
                    target_table=scenario.get('target_table', scenario['source_table']),
                    source_join_key=scenario.get('source_join_key', 'id'),
                    target_join_key=scenario.get('target_join_key', 'id'),
                    target_column=scenario['target_column'],
                    derivation_logic=scenario['derivation_logic'],
                    reference_table=scenario['reference_table'],
                    reference_join_key=scenario.get('reference_join_key', 'id'),
                    reference_lookup_column=scenario.get('reference_lookup_column', 'value'),
                    reference_return_column=scenario.get('reference_return_column', 'value'),
                    business_conditions=scenario.get('business_conditions', ''),
                    hardcoded_values=scenario.get('hardcoded_values', ''),
                    project_id='cohesive-apogee-411113',
                    dataset_id='banking_sample_data'
                )
            elif scenario.get('target_table') and str(scenario.get('target_table')).lower() not in ['nan', 'none', '']:
                # Enhanced transformation validation
                sql_query = create_enhanced_transformation_sql(
                    source_table=scenario['source_table'],
                    target_table=scenario['target_table'],
                    source_join_key=scenario.get('source_join_key', 'id'),
                    target_join_key=scenario.get('target_join_key', 'id'),
                    target_column=scenario['target_column'],
                    derivation_logic=scenario['derivation_logic'],
                    project_id='cohesive-apogee-411113',
                    dataset_id='banking_sample_data'
                )
            else:
                # Basic transformation validation
                sql_query = create_transformation_validation_sql(
                    source_table=scenario['source_table'],
                    target_table=scenario.get('target_table', scenario['source_table']),
                    source_join_key=scenario.get('source_join_key', 'id'),
                    target_join_key=scenario.get('target_join_key', 'id'),
                    target_column=scenario.get('target_column', 'derived_value'),
                    derivation_logic=scenario['derivation_logic'],
                    project_id='cohesive-apogee-411113',
                    dataset_id='banking_sample_data'
                )
            
            # Execute the query
            if sql_query:
                query_result, message = execute_custom_query(sql_query, scenario['scenario_name'])
                
                if query_result and query_result['status'] == 'success':
                    df = query_result['data']
                    
                    if df is not None and not df.empty:
                        # Determine pass/fail based on results
                        if 'validation_status' in df.columns:
                            # New format with validation_status column
                            status = df.iloc[0]['validation_status']
                            passed_count = df.iloc[0].get('row_count', 1) if status == 'PASS' else 0
                            total_count = df.iloc[0].get('row_count', 1)
                        elif 'validation_result' in df.columns:
                            # Old format with validation_result column
                            passed_count = len(df[df['validation_result'] == 'PASS'])
                            total_count = len(df)
                            status = 'PASS' if passed_count == total_count else 'FAIL'
                        else:
                            # If no validation columns, check if we have any rows (failures)
                            status = 'FAIL' if len(df) > 0 else 'PASS'
                            passed_count = 0 if len(df) > 0 else 1
                            total_count = max(1, len(df))
                        
                        results.append({
                            'scenario_name': scenario['scenario_name'],
                            'status': status,
                            'total_records': total_count,
                            'passed_records': passed_count,
                            'sql_query': sql_query,
                            'result_data': df,
                            'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    else:
                        results.append({
                            'scenario_name': scenario['scenario_name'],
                            'status': 'PASS',  # No data usually means no issues found
                            'total_records': 0,
                            'passed_records': 0,
                            'sql_query': sql_query,
                            'result_data': pd.DataFrame(),
                            'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                else:
                    # Query execution failed
                    error_msg = query_result.get('error', 'Unknown error') if query_result else 'Query execution failed'
                    results.append({
                        'scenario_name': scenario['scenario_name'],
                        'status': 'ERROR',
                        'error_message': error_msg,
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


def get_scenario_type(scenario: Dict[str, Any]) -> str:
    """Determine the type of validation scenario."""
    if scenario.get('reference_table') and str(scenario.get('reference_table')).lower() not in ['nan', 'none', '']:
        return 'Reference Table'
    elif scenario.get('target_table') and str(scenario.get('target_table')).lower() not in ['nan', 'none', '']:
        return 'Enhanced Transformation'
    else:
        return 'Basic Transformation'


def generate_sql_for_scenario(scenario: Dict[str, Any], project_id: str = 'cohesive-apogee-411113', dataset_id: str = 'banking_sample_data') -> str:
    """Generate SQL for a specific scenario for preview purposes."""
    try:
        # Generate SQL based on scenario type
        if scenario.get('reference_table') and str(scenario.get('reference_table')).lower() not in ['nan', 'none', '']:
            # Reference table validation
            sql_query = create_reference_table_validation_sql(
                source_table=scenario['source_table'],
                target_table=scenario.get('target_table', scenario['source_table']),
                source_join_key=scenario.get('source_join_key', 'id'),
                target_join_key=scenario.get('target_join_key', 'id'),
                target_column=scenario['target_column'],
                derivation_logic=scenario['derivation_logic'],
                reference_table=scenario['reference_table'],
                reference_join_key=scenario.get('reference_join_key', 'id'),
                reference_lookup_column=scenario.get('reference_lookup_column', 'value'),
                reference_return_column=scenario.get('reference_return_column', 'value'),
                business_conditions=scenario.get('business_conditions', ''),
                hardcoded_values=scenario.get('hardcoded_values', ''),
                project_id=project_id,
                dataset_id=dataset_id
            )
        elif scenario.get('target_table') and str(scenario.get('target_table')).lower() not in ['nan', 'none', '']:
            # Enhanced transformation validation
            sql_query = create_enhanced_transformation_sql(
                source_table=scenario['source_table'],
                target_table=scenario['target_table'],
                source_join_key=scenario.get('source_join_key', 'id'),
                target_join_key=scenario.get('target_join_key', 'id'),
                target_column=scenario['target_column'],
                derivation_logic=scenario['derivation_logic'],
                project_id=project_id,
                dataset_id=dataset_id
            )
        else:
            # Basic transformation validation
            sql_query = create_transformation_validation_sql(
                source_table=scenario['source_table'],
                target_table=scenario.get('target_table', scenario['source_table']),
                source_join_key=scenario.get('source_join_key', 'id'),
                target_join_key=scenario.get('target_join_key', 'id'),
                target_column=scenario.get('target_column', 'derived_value'),
                derivation_logic=scenario['derivation_logic'],
                project_id=project_id,
                dataset_id=dataset_id
            )
        
        return sql_query if sql_query else "-- SQL generation failed"
        
    except Exception as e:
        return f"-- Error generating SQL: {str(e)}"
