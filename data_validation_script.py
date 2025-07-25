#!/usr/bin/env python3
"""
Data Validation Script for Banking Domain - Table Comparisons
============================================================

This script processes an Excel mapping file to validate data consistency between 
source and target tables. It supports both local testing (without BigQuery) and 
production execution using BigQuery.

USAGE:
    Test Mode (Local simulation):
        python data_validation_script.py --excel mapping.xlsx --test True
    
    Production Mode (BigQuery):
        python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id

EXCEL FILE STRUCTURE:
    - Table Name: Name of the table being validated
    - Source Column Name: Column name in source table
    - Target Column Name: Column name in target table  
    - Transformation Logic: Description of transformation (e.g., 'copy', 'derived using col A + B')
    - Join Condition: SQL condition to join source and target tables
    - Optional WHERE Clause: Additional filtering conditions

OUTPUT:
    - summary_results.csv: Summary of validation results
    - validation_logs.log: Detailed timestamped logs

AUTHOR: Banking Domain Expert & Python Developer
DATE: July 2025
"""

import pandas as pd
import numpy as np
import argparse
import logging
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re

# BigQuery imports (will handle import error in test mode)
try:
    from google.cloud import bigquery
    from google.oauth2 import service_account
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False
    print("Warning: BigQuery libraries not available. Running in test mode only.")

class DataValidationProcessor:
    """Main class for processing data validation between source and target tables."""
    
    def __init__(self, test_mode: bool = True, project_id: Optional[str] = None, 
                 credentials_path: Optional[str] = None, project_info: Optional[Dict[str, str]] = None):
        """
        Initialize the data validation processor.
        
        Args:
            test_mode: If True, simulate using pandas DataFrames. If False, use BigQuery.
            project_id: BigQuery project ID (required for production mode)
            credentials_path: Path to BigQuery credentials JSON file
            project_info: Dictionary containing project configuration
        """
        self.test_mode = test_mode
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.project_info = project_info or {'Project': project_id, 'Source': 'Baseline'}
        self.client = None
        self.sheet_name = 'Default Data'
        
        # Setup logging
        self.setup_logging()
        
        # Initialize BigQuery client if in production mode
        if not test_mode:
            self.setup_bigquery_client()
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_filename = f"validation_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Data Validation Processor initialized successfully")
    
    def bigquery_connect(self, project_info: Dict[str, str]) -> Tuple[object, str]:
        """
        Setup BigQuery client for production mode using office-proven connection method.
        
        Args:
            project_info: Dictionary containing project configuration
            
        Returns:
            Tuple of (client, sheet_name)
        """
        if not BIGQUERY_AVAILABLE:
            raise ImportError("BigQuery libraries not available. Install google-cloud-bigquery.")
        
        try:
            if "prod" in project_info['Project']:
                project = project_info['Project']
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                ) if self.credentials_path else None
                
                if credentials:
                    client = bigquery.Client(credentials=credentials, project=project)
                else:
                    # Use default credentials
                    import google.auth
                    credentials, _ = google.auth.default()
                    client = bigquery.Client(credentials=credentials, project=project)
                
                self.logger.info("BIGQUERY prod client connected")
                
            elif "dev" in project_info['Project']:
                # Set environment variables for development proxy
                import os
                # Configure these proxy settings for your enterprise network
                os.environ["HTTP_PROXY"] = "your-enterprise-proxy:port"
                os.environ["HTTPS_PROXY"] = "your-enterprise-proxy:port"
                project = project_info['Project']
                
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                ) if self.credentials_path else None
                
                if credentials:
                    client = bigquery.Client(credentials=credentials, project=project)
                else:
                    # Use default credentials
                    import google.auth
                    credentials, _ = google.auth.default()
                    client = bigquery.Client(credentials=credentials, project=project)
                
                self.logger.info("BIGQUERY dev client connected")
            
            else:
                # Fallback for other environments
                client = bigquery.Client(project=self.project_id)
                self.logger.info(f"BIGQUERY client connected for project: {self.project_id}")
            
            # Determine sheet name based on source
            if project_info.get('Source') == 'Test':
                sheet_name = 'Test Data'
            elif project_info.get('Source') == 'Baseline':
                sheet_name = 'Production Data'
            else:
                sheet_name = 'Default Data'
            
            self.client = client
            return client, sheet_name
            
        except Exception as e:
            self.logger.error(f"Failed to initialize BigQuery client: {str(e)}")
            raise
    
    def setup_bigquery_client(self):
        """Setup BigQuery client for production mode using the office connection method."""
        self.client, self.sheet_name = self.bigquery_connect(self.project_info)
        self.logger.info(f"BigQuery client initialized for project: {self.project_info['Project']}")
        self.logger.info(f"Using data source: {self.sheet_name}")
    
    def load_excel_mapping(self, excel_path: str) -> pd.DataFrame:
        """
        Load the Excel mapping file with the expected structure from the screenshot.
        
        Expected columns: Version, Function, Target Table, Target Attribute, Derivation, Derivation Type, Primary
        
        Args:
            excel_path: Path to the Excel mapping file
            
        Returns:
            DataFrame containing the mapping data
        """
        try:
            df = pd.read_excel(excel_path)
            self.logger.info(f"Successfully loaded Excel file: {excel_path}")
            self.logger.info(f"Number of mappings loaded: {len(df)}")
            
            # Log the actual columns found
            self.logger.info(f"Columns found: {list(df.columns)}")
            
            # Check for expected columns based on the screenshot
            expected_columns = ['Version', 'Function', 'Target Table', 'Target Attribute', 'Derivation', 'Derivation Type']
            
            # Try to find columns that match our expected structure (case-insensitive)
            column_mapping = {}
            for expected_col in expected_columns:
                for actual_col in df.columns:
                    if expected_col.lower() in str(actual_col).lower():
                        column_mapping[expected_col] = actual_col
                        break
            
            self.logger.info(f"Column mapping: {column_mapping}")
            
            # Create standardized column names for internal processing
            if 'Target Table' in column_mapping and 'Target Attribute' in column_mapping:
                df['Table_Name'] = df[column_mapping['Target Table']]
                df['Target_Column'] = df[column_mapping['Target Attribute']]
            
            if 'Derivation' in column_mapping:
                df['Source_Column'] = df[column_mapping['Derivation']]
                df['Transformation_Logic'] = df[column_mapping.get('Derivation Type', column_mapping['Derivation'])]
            
            # Create a default join condition based on table structure
            if 'Table_Name' in df.columns:
                df['Join_Condition'] = df['Table_Name'].apply(lambda x: f's.id = t.id' if pd.notna(x) else '')
            else:
                df['Join_Condition'] = 's.id = t.id'
            
            # Add Optional WHERE Clause column if not present
            df['Optional_WHERE_Clause'] = ''
            
            # Filter out rows where essential data is missing
            df = df.dropna(subset=['Table_Name', 'Target_Column', 'Source_Column'])
            
            self.logger.info(f"Processed mappings: {len(df)}")
            return df
        
        except Exception as e:
            self.logger.error(f"Failed to load Excel file: {str(e)}")
            raise
    
    def generate_sql_case_statement(self, source_col: str, target_col: str, 
                                  transformation_logic: str) -> str:
        """
        Generate SQL CASE statement for comparison.
        
        Args:
            source_col: Source column name
            target_col: Target column name
            transformation_logic: Description of transformation logic
            
        Returns:
            SQL CASE statement string
        """
        # Clean column names (remove any brackets or special characters for SQL)
        source_col_clean = re.sub(r'[^\w]', '_', source_col)
        target_col_clean = re.sub(r'[^\w]', '_', target_col)
        
        # Handle different transformation logic types
        if transformation_logic.lower().strip() in ['copy', 'direct copy', 'same']:
            # Direct comparison
            case_statement = f"""CASE 
                WHEN s.{source_col_clean} = t.{target_col_clean} THEN 'PASS' 
                WHEN s.{source_col_clean} IS NULL AND t.{target_col_clean} IS NULL THEN 'PASS'
                ELSE 'FAIL' 
            END"""
        
        elif 'derived using' in transformation_logic.lower():
            # Extract formula from transformation logic
            # This is a simplified approach - in production, you'd want more robust parsing
            formula_match = re.search(r'derived using (.+)', transformation_logic, re.IGNORECASE)
            if formula_match:
                formula = formula_match.group(1).strip()
                # Replace column references with s.column_name format
                formula_sql = self.parse_formula_to_sql(formula)
                case_statement = f"""CASE 
                    WHEN ({formula_sql}) = t.{target_col_clean} THEN 'PASS'
                    WHEN ({formula_sql}) IS NULL AND t.{target_col_clean} IS NULL THEN 'PASS'
                    ELSE 'FAIL' 
                END"""
            else:
                # Fallback to direct comparison
                case_statement = f"""CASE 
                    WHEN s.{source_col_clean} = t.{target_col_clean} THEN 'PASS' 
                    ELSE 'FAIL' 
                END"""
        
        else:
            # Default case for other transformation types
            case_statement = f"""CASE 
                WHEN s.{source_col_clean} = t.{target_col_clean} THEN 'PASS' 
                WHEN s.{source_col_clean} IS NULL AND t.{target_col_clean} IS NULL THEN 'PASS'
                ELSE 'FAIL' 
            END"""
        
        return case_statement + f" AS {source_col_clean}_validation_result"
    
    def parse_formula_to_sql(self, formula: str) -> str:
        """
        Parse a formula description to SQL.
        
        Args:
            formula: Formula description (e.g., "col A + col B")
            
        Returns:
            SQL expression
        """
        # Simple parsing - replace "col X" with "s.X"
        # In production, you'd want more sophisticated parsing
        formula_sql = re.sub(r'\bcol\s+(\w+)', r's.\1', formula, flags=re.IGNORECASE)
        return formula_sql
    
    def generate_validation_sql(self, row: pd.Series) -> str:
        """
        Generate complete validation SQL for a mapping row.
        
        Args:
            row: DataFrame row containing mapping information
            
        Returns:
            Complete SQL query string
        """
        table_name = row['Table_Name']
        source_col = row['Source_Column'] 
        target_col = row['Target_Column']
        transformation_logic = row['Transformation_Logic']
        join_condition = row['Join_Condition']
        where_clause = row.get('Optional_WHERE_Clause', '')
        
        # Generate CASE statement
        case_statement = self.generate_sql_case_statement(source_col, target_col, transformation_logic)
        
        # Build the complete SQL
        sql_parts = []
        sql_parts.append("SELECT")
        sql_parts.append("    COUNT(*) AS total_count,")
        sql_parts.append(f"    SUM(CASE WHEN ({case_statement.split(' AS ')[0]}) = 'PASS' THEN 1 ELSE 0 END) AS pass_count,")
        sql_parts.append(f"    SUM(CASE WHEN ({case_statement.split(' AS ')[0]}) = 'FAIL' THEN 1 ELSE 0 END) AS fail_count")
        sql_parts.append(f"FROM {table_name}_source s")
        sql_parts.append(f"JOIN {table_name}_target t ON {join_condition}")
        
        if where_clause and where_clause.strip():
            sql_parts.append(f"WHERE {where_clause}")
        
        complete_sql = "\n".join(sql_parts)
        return complete_sql
    
    def create_sample_dataframes(self, table_name: str, source_col: str, target_col: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Create sample DataFrames for testing.
        
        Args:
            table_name: Name of the table
            source_col: Source column name
            target_col: Target column name
            
        Returns:
            Tuple of (source_df, target_df)
        """
        np.random.seed(42)  # For reproducible results
        
        # Create sample data
        n_records = 1000
        
        # Generate primary keys
        ids = list(range(1, n_records + 1))
        
        # Create source data with 'source_' prefix to avoid naming conflicts
        source_data = {
            'id': ids,
            f'source_{source_col}': np.random.choice(['A', 'B', 'C', None], n_records, p=[0.4, 0.3, 0.2, 0.1])
        }
        
        # Create target data with 'target_' prefix (with some intentional mismatches for testing)
        target_data = {
            'id': ids,
            f'target_{target_col}': np.random.choice(['A', 'B', 'C', 'D', None], n_records, p=[0.35, 0.25, 0.15, 0.15, 0.1])
        }
        
        source_df = pd.DataFrame(source_data)
        target_df = pd.DataFrame(target_data)
        
        self.logger.info(f"Created sample DataFrames for {table_name} with {n_records} records each")
        
        return source_df, target_df
    
    def simulate_validation(self, row: pd.Series) -> Dict[str, int]:
        """
        Simulate validation using pandas DataFrames.
        
        Args:
            row: DataFrame row containing mapping information
            
        Returns:
            Dictionary with validation results
        """
        table_name = row['Table_Name']
        source_col = row['Source_Column']
        target_col = row['Target_Column']
        transformation_logic = row['Transformation_Logic']
        
        # Create sample dataframes
        source_df, target_df = self.create_sample_dataframes(table_name, source_col, target_col)
        
        # Simulate join on 'id' column
        merged_df = pd.merge(source_df, target_df, on='id', how='inner')
        
        # Use prefixed column names for comparison
        source_col_name = f'source_{source_col}'
        target_col_name = f'target_{target_col}'
        
        # Apply validation logic based on derivation type or logic
        if pd.isna(transformation_logic) or str(transformation_logic).lower().strip() in ['copy', 'direct copy', 'same', '']:
            # Direct comparison
            merged_df['validation_result'] = np.where(
                merged_df[source_col_name] == merged_df[target_col_name], 'PASS', 
                np.where(
                    (merged_df[source_col_name].isna()) & (merged_df[target_col_name].isna()), 'PASS', 'FAIL'
                )
            )
        else:
            # For other transformation types, use direct comparison as default
            # In a real scenario, you'd parse the derivation formula
            merged_df['validation_result'] = np.where(
                merged_df[source_col_name] == merged_df[target_col_name], 'PASS', 'FAIL'
            )
        
        # Calculate results
        total_count = len(merged_df)
        pass_count = len(merged_df[merged_df['validation_result'] == 'PASS'])
        fail_count = len(merged_df[merged_df['validation_result'] == 'FAIL'])
        
        return {
            'total_count': total_count,
            'pass_count': pass_count,
            'fail_count': fail_count
        }
    
    def execute_bigquery_validation(self, sql_query: str) -> Dict[str, int]:
        """
        Execute validation using BigQuery.
        
        Args:
            sql_query: SQL query to execute
            
        Returns:
            Dictionary with validation results
        """
        try:
            query_job = self.client.query(sql_query)
            results = query_job.result()
            
            # Extract results
            for row in results:
                return {
                    'total_count': row.total_count,
                    'pass_count': row.pass_count,
                    'fail_count': row.fail_count
                }
            
            # If no results, return zeros
            return {'total_count': 0, 'pass_count': 0, 'fail_count': 0}
        
        except Exception as e:
            self.logger.error(f"BigQuery execution failed: {str(e)}")
            raise
    
    def process_mappings(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process all mappings and generate validation results.
        
        Args:
            df: DataFrame containing mapping data
            
        Returns:
            DataFrame with validation results
        """
        results = []
        
        # Add SQL_Case_Statement column
        df['SQL_Case_Statement'] = df.apply(
            lambda row: self.generate_sql_case_statement(
                row['Source_Column'], 
                row['Target_Column'], 
                row['Transformation_Logic']
            ), axis=1
        )
        
        for idx, row in df.iterrows():
            self.logger.info(f"Processing mapping {idx + 1}/{len(df)}: {row['Table_Name']} - {row['Source_Column']}")
            
            try:
                if self.test_mode:
                    # Simulate validation
                    validation_results = self.simulate_validation(row)
                else:
                    # Execute BigQuery validation
                    sql_query = self.generate_validation_sql(row)
                    self.logger.info(f"Executing SQL: {sql_query}")
                    validation_results = self.execute_bigquery_validation(sql_query)
                
                # Prepare result row
                result_row = {
                    'Table_Name': row['Table_Name'],
                    'Source_Column': row['Source_Column'],
                    'Target_Column': row['Target_Column'],
                    'Transformation_Logic': row['Transformation_Logic'],
                    'Total_Count': validation_results['total_count'],
                    'Pass_Count': validation_results['pass_count'],
                    'Fail_Count': validation_results['fail_count'],
                    'Pass_Rate': (validation_results['pass_count'] / validation_results['total_count'] * 100) if validation_results['total_count'] > 0 else 0,
                    'Status': 'PASS' if validation_results['fail_count'] == 0 else 'FAIL'
                }
                
                results.append(result_row)
                self.logger.info(f"Completed mapping {idx + 1}: {result_row['Status']} - Pass Rate: {result_row['Pass_Rate']:.2f}%")
                
            except Exception as e:
                self.logger.error(f"Failed to process mapping {idx + 1}: {str(e)}")
                # Add error result
                error_row = {
                    'Table_Name': row['Table_Name'],
                    'Source_Column': row['Source_Column'],
                    'Target_Column': row['Target_Column'],
                    'Transformation_Logic': row['Transformation_Logic'],
                    'Total_Count': 0,
                    'Pass_Count': 0,
                    'Fail_Count': 0,
                    'Pass_Rate': 0,
                    'Status': 'ERROR'
                }
                results.append(error_row)
        
        results_df = pd.DataFrame(results)
        return results_df
    
    def save_results(self, results_df: pd.DataFrame, updated_mapping_df: pd.DataFrame):
        """
        Save validation results and updated mapping file.
        
        Args:
            results_df: DataFrame with validation results
            updated_mapping_df: Updated mapping DataFrame with SQL_Case_Statement column
        """
        # Save summary results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_filename = f"summary_results_{timestamp}.csv"
        results_df.to_csv(summary_filename, index=False)
        self.logger.info(f"Summary results saved to: {summary_filename}")
        
        # Save updated mapping file
        mapping_filename = f"updated_mapping_{timestamp}.xlsx"
        updated_mapping_df.to_excel(mapping_filename, index=False)
        self.logger.info(f"Updated mapping file saved to: {mapping_filename}")
        
        # Print summary statistics
        total_mappings = len(results_df)
        passed_mappings = len(results_df[results_df['Status'] == 'PASS'])
        failed_mappings = len(results_df[results_df['Status'] == 'FAIL'])
        error_mappings = len(results_df[results_df['Status'] == 'ERROR'])
        
        print(f"\n{'='*50}")
        print("VALIDATION SUMMARY")
        print(f"{'='*50}")
        print(f"Total Mappings Processed: {total_mappings}")
        print(f"Passed Validations: {passed_mappings}")
        print(f"Failed Validations: {failed_mappings}")
        print(f"Error Mappings: {error_mappings}")
        print(f"Overall Success Rate: {(passed_mappings/total_mappings*100):.2f}%" if total_mappings > 0 else "N/A")
        print(f"{'='*50}")


def main():
    """Main function to handle command line arguments and execute the validation process."""
    parser = argparse.ArgumentParser(
        description="Data Validation Script for Banking Domain - Table Comparisons",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    Test Mode (Local simulation):
        python data_validation_script.py --excel mapping.xlsx --test True
    
    Production Mode (BigQuery Production):
        python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id --environment prod
    
    Development Mode (BigQuery Development with proxy):
        python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id --environment dev
        
    With credentials file:
        python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id --credentials path/to/credentials.json --environment prod
        
    Using test data source:
        python data_validation_script.py --excel mapping.xlsx --test False --project your-project-id --source Test --environment dev
        """
    )
    
    parser.add_argument('--excel', required=True, help='Path to Excel mapping file')
    parser.add_argument('--test', type=str, choices=['True', 'False'], default='True', 
                       help='Test mode flag (True for local simulation, False for BigQuery)')
    parser.add_argument('--project', help='BigQuery project ID (required for production mode)')
    parser.add_argument('--credentials', help='Path to BigQuery credentials JSON file')
    parser.add_argument('--source', choices=['Test', 'Baseline'], default='Baseline',
                       help='Data source type (Test for test data, Baseline for production data)')
    parser.add_argument('--environment', choices=['prod', 'dev'], default='prod',
                       help='Environment type (prod for production, dev for development with proxy)')
    
    args = parser.parse_args()
    
    # Convert test flag to boolean
    test_mode = args.test == 'True'
    
    # Validate arguments
    if not test_mode and not args.project:
        parser.error("BigQuery project ID is required when test mode is False")
    
    if not os.path.exists(args.excel):
        parser.error(f"Excel file not found: {args.excel}")
    
    # Prepare project info for BigQuery connection
    project_info = {
        'Project': args.project if args.project else 'default-project',
        'Source': args.source
    }
    
    # Add environment indicator to project name for connection logic
    if not test_mode and args.project:
        if args.environment == 'dev' and 'dev' not in args.project.lower():
            project_info['Project'] = f"{args.project}-dev"
        elif args.environment == 'prod' and 'prod' not in args.project.lower():
            project_info['Project'] = f"{args.project}-prod"
    
    try:
        # Initialize processor
        processor = DataValidationProcessor(
            test_mode=test_mode,
            project_id=args.project,
            credentials_path=args.credentials,
            project_info=project_info
        )
        
        # Load Excel mapping
        mapping_df = processor.load_excel_mapping(args.excel)
        
        # Process mappings
        results_df = processor.process_mappings(mapping_df)
        
        # Save results
        processor.save_results(results_df, mapping_df)
        
        print("\nValidation process completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
