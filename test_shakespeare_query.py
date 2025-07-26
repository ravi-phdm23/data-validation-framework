#!/usr/bin/env python3
"""
Test script to connect to BigQuery and run a Shakespeare query
Project ID: cohesive-apogee-411113
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
        logging.FileHandler(f'bigquery_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)
logger = logging.getLogger(__name__)

def test_bigquery_connection():
    """Test BigQuery connection and run Shakespeare query."""
    
    project_id = "cohesive-apogee-411113"
    
    try:
        # Import BigQuery libraries
        logger.info("Importing BigQuery libraries...")
        from google.cloud import bigquery
        import google.auth
        logger.info("✅ BigQuery libraries imported successfully")
        
        # Initialize BigQuery client
        logger.info(f"Initializing BigQuery client for project: {project_id}")
        
        try:
            # Try to use default credentials first
            client = bigquery.Client(project=project_id)
            logger.info("✅ BigQuery client initialized using default credentials")
        except Exception as e:
            logger.error(f"❌ Failed to initialize with default credentials: {e}")
            logger.info("Attempting to use application default credentials...")
            
            # Try with explicit credential loading
            credentials, project = google.auth.default()
            client = bigquery.Client(credentials=credentials, project=project_id)
            logger.info("✅ BigQuery client initialized using application default credentials")
        
        # Test the connection with the Shakespeare query
        logger.info("Testing connection with Shakespeare query...")
        
        query = """
        SELECT word, word_count
        FROM `bigquery-public-data.samples.shakespeare`
        ORDER BY word_count DESC
        LIMIT 5
        """
        
        logger.info("Executing query:")
        logger.info(query)
        
        # Run the query
        query_job = client.query(query)
        results = query_job.result()
        
        logger.info("✅ Query executed successfully!")
        logger.info("Results:")
        logger.info("-" * 50)
        
        # Display results
        for i, row in enumerate(results, 1):
            logger.info(f"{i}. Word: {row.word}, Count: {row.word_count}")
            print(f"{i}. Word: {row.word}, Count: {row.word_count}")
        
        logger.info("-" * 50)
        logger.info("🎉 BigQuery connection test completed successfully!")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Missing BigQuery dependencies: {e}")
        logger.error("Please install required packages:")
        logger.error("pip install google-cloud-bigquery google-auth")
        return False
        
    except Exception as e:
        logger.error(f"❌ BigQuery connection test failed: {e}")
        logger.error("Common solutions:")
        logger.error("1. Ensure you're authenticated with Google Cloud:")
        logger.error("   gcloud auth application-default login")
        logger.error("2. Or set up a service account:")
        logger.error("   export GOOGLE_APPLICATION_CREDENTIALS='path/to/service-account.json'")
        logger.error("3. Verify the project ID is correct: cohesive-apogee-411113")
        logger.error("4. Check if BigQuery API is enabled in your project")
        return False

def check_authentication_status():
    """Check current authentication status."""
    logger.info("Checking authentication status...")
    
    # Check if gcloud is configured
    try:
        import subprocess
        result = subprocess.run(['gcloud', 'auth', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info("gcloud authentication status:")
            logger.info(result.stdout)
        else:
            logger.warning("gcloud not configured or not found")
    except Exception as e:
        logger.warning(f"Could not check gcloud status: {e}")
    
    # Check environment variables
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        logger.info(f"GOOGLE_APPLICATION_CREDENTIALS: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
    else:
        logger.info("GOOGLE_APPLICATION_CREDENTIALS not set")

if __name__ == "__main__":
    print("🔍 BigQuery Connection Test for Shakespeare Query")
    print("=" * 60)
    print(f"Project ID: cohesive-apogee-411113")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check authentication first
    check_authentication_status()
    print()
    
    # Run the test
    success = test_bigquery_connection()
    
    if success:
        print("\n🎉 SUCCESS: BigQuery connection test passed!")
    else:
        print("\n❌ FAILED: BigQuery connection test failed. Check the logs for details.")
