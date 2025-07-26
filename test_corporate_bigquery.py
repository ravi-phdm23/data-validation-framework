#!/usr/bin/env python3
"""
Corporate Office BigQuery Connection Test
Test script specifically designed for office/corporate network environments
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'corporate_bigquery_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

def test_corporate_bigquery_connection():
    """Test BigQuery connection using corporate office setup."""
    
    print("🏢 Corporate Office BigQuery Connection Test")
    print("=" * 60)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Step 1: Import required libraries
        logger.info("Importing BigQuery libraries...")
        from google.cloud import bigquery
        import google.auth
        logger.info("✅ BigQuery libraries imported successfully")
        
        # Step 2: Set up corporate proxy environment
        logger.info("Setting up corporate proxy environment...")
        
        # Corporate proxy settings (based on your screenshot)
        corporate_proxies = {
            "HTTP_PROXY": "googleapis-dev.gcp.cloud.uk.hsbc:3128",
            "HTTPS_PROXY": "googleapis-dev.gcp.cloud.uk.hsbc:3128"
        }
        
        for key, value in corporate_proxies.items():
            if not os.environ.get(key):
                os.environ[key] = value
                logger.info(f"Set {key} = {value}")
        
        logger.info("✅ Corporate proxy environment configured")
        
        # Step 3: Test different project configurations
        test_projects = [
            "cohesive-apogee-411113",  # Your current project
            "sbc-90930858-rwapc52-dev"  # Project from your screenshot
        ]
        
        for project_id in test_projects:
            print(f"\n🔍 Testing project: {project_id}")
            logger.info(f"Testing BigQuery connection for project: {project_id}")
            
            try:
                # Method 1: Try with default credentials and project detection
                logger.info("Method 1: Default credentials with project detection...")
                credentials, detected_project = google.auth.default()
                
                # Use detected project or specified project
                final_project = detected_project if detected_project else project_id
                logger.info(f"Using project: {final_project}")
                
                # Create BigQuery client
                client = bigquery.Client(credentials=credentials, project=final_project)
                logger.info("BigQuery client created successfully")
                
                # Test with a simple query
                test_query = "SELECT 1 as test_connection, CURRENT_TIMESTAMP() as test_time"
                logger.info("Executing test query...")
                
                query_job = client.query(test_query)
                results = list(query_job.result())
                
                if results:
                    result = results[0]
                    print(f"✅ SUCCESS for {final_project}!")
                    print(f"   Test Connection: {result.test_connection}")
                    print(f"   Server Time: {result.test_time}")
                    logger.info(f"✅ Test query successful for project: {final_project}")
                    
                    # Try to access your banking dataset if it exists
                    try:
                        dataset_query = f"""
                        SELECT table_name, row_count
                        FROM `{final_project}.banking_sample_data.INFORMATION_SCHEMA.TABLE_STORAGE`
                        WHERE table_name IN ('customers', 'transactions')
                        """
                        
                        dataset_job = client.query(dataset_query)
                        dataset_results = list(dataset_job.result())
                        
                        if dataset_results:
                            print("📊 Banking Dataset Found:")
                            for row in dataset_results:
                                print(f"   Table: {row.table_name}, Rows: {row.row_count}")
                        else:
                            print("📊 Banking dataset not found (this is okay for testing)")
                            
                    except Exception as dataset_error:
                        print("📊 Banking dataset check skipped (this is okay for testing)")
                        logger.info(f"Dataset check skipped: {dataset_error}")
                    
                    return True, final_project
                    
                else:
                    logger.warning(f"No results returned for project: {final_project}")
                    
            except Exception as project_error:
                logger.error(f"❌ Failed for project {project_id}: {project_error}")
                print(f"❌ Failed for {project_id}: {project_error}")
                continue
        
        return False, None
        
    except ImportError as e:
        error_msg = f"❌ Missing BigQuery dependencies: {e}"
        logger.error(error_msg)
        print(error_msg)
        print("Please install: pip install google-cloud-bigquery google-auth")
        return False, None
        
    except Exception as e:
        error_msg = f"❌ Corporate BigQuery test failed: {e}"
        logger.error(error_msg)
        print(error_msg)
        
        print("\n🔧 Troubleshooting for Corporate Networks:")
        print("1. Verify you're connected to the corporate VPN")
        print("2. Check if your IT team has configured Google API access")
        print("3. Ensure BigQuery API is enabled in your project")
        print("4. Verify the proxy URLs are correct for your network")
        print("5. Try running: gcloud auth application-default login")
        
        return False, None

def test_proxy_connectivity():
    """Test if the proxy settings allow connection to Google APIs."""
    print("\n🌐 Testing Proxy Connectivity")
    print("-" * 40)
    
    try:
        import requests
        
        # Test proxy connectivity
        proxies = {
            'http': os.environ.get('HTTP_PROXY'),
            'https': os.environ.get('HTTPS_PROXY')
        }
        
        if proxies['http'] or proxies['https']:
            print(f"Using proxies: {proxies}")
            
            # Test connection to Google APIs
            test_url = "https://www.googleapis.com"
            response = requests.get(test_url, proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                print("✅ Proxy connection to Google APIs successful")
                return True
            else:
                print(f"⚠️ Proxy connection returned status: {response.status_code}")
                return False
        else:
            print("No proxy settings detected")
            return True
            
    except Exception as e:
        print(f"❌ Proxy connectivity test failed: {e}")
        return False

if __name__ == "__main__":
    # Test proxy connectivity first
    proxy_ok = test_proxy_connectivity()
    
    # Run BigQuery connection test
    success, project = test_corporate_bigquery_connection()
    
    print("\n" + "=" * 60)
    if success:
        print(f"🎉 CORPORATE BIGQUERY CONNECTION SUCCESSFUL!")
        print(f"✅ Connected to project: {project}")
        print("You can now use this configuration in the Streamlit app")
    else:
        print("❌ CORPORATE BIGQUERY CONNECTION FAILED")
        print("Check the logs above for specific error details")
    print("=" * 60)
