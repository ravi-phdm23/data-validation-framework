#!/usr/bin/env python3
"""
Corporate BigQuery Configuration
Specialized setup for office/corporate environments with proxy settings
"""

import os
import logging
from google.cloud import bigquery
import google.auth

logger = logging.getLogger(__name__)

class CorporateBigQueryConfig:
    """
    Corporate BigQuery configuration handler for office environments.
    Handles proxy settings, project detection, and authentication.
    """
    
    def __init__(self):
        self.proxy_settings = {
            # Default corporate proxy settings (modify as needed)
            "HTTP_PROXY": "googleapis-dev.gcp.cloud.uk.hsbc:3128",
            "HTTPS_PROXY": "googleapis-dev.gcp.cloud.uk.hsbc:3128"
        }
        
        # Corporate project patterns
        self.corporate_indicators = [
            'dev', 'prod', 'test', 'staging', 
            'corp', 'enterprise', 'hsbc', 'bank'
        ]
    
    def is_corporate_environment(self, project_id=None):
        """Check if this appears to be a corporate environment."""
        indicators = [
            # Check project ID patterns
            project_id and any(indicator in project_id.lower() for indicator in self.corporate_indicators),
            # Check if proxy environment variables are set
            os.environ.get("HTTP_PROXY") is not None,
            os.environ.get("HTTPS_PROXY") is not None,
            # Check for corporate domain patterns
            os.environ.get("USERDOMAIN", "").lower() in ['corp', 'enterprise', 'hsbc'],
            # Check for specific corporate environment variables
            os.environ.get("CORPORATE_NETWORK") == "true"
        ]
        
        return any(indicators)
    
    def setup_proxy_environment(self):
        """Configure proxy environment variables for corporate network."""
        try:
            for key, value in self.proxy_settings.items():
                if not os.environ.get(key):
                    os.environ[key] = value
                    logger.info(f"Set {key} = {value}")
            
            logger.info("✅ Corporate proxy environment configured")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup proxy environment: {e}")
            return False
    
    def get_corporate_credentials(self):
        """Get credentials using corporate authentication flow."""
        try:
            # Method 1: Try default credentials with project detection
            credentials, project = google.auth.default()
            logger.info(f"✅ Default credentials loaded, detected project: {project}")
            return credentials, project
            
        except Exception as e:
            logger.error(f"❌ Corporate credentials failed: {e}")
            raise
    
    def create_corporate_client(self, project_id=None):
        """Create BigQuery client optimized for corporate environment."""
        try:
            logger.info("🏢 Initializing corporate BigQuery client...")
            
            # Step 1: Setup proxy if corporate environment
            if self.is_corporate_environment(project_id):
                logger.info("📡 Corporate environment detected")
                self.setup_proxy_environment()
            
            # Step 2: Get credentials
            credentials, detected_project = self.get_corporate_credentials()
            
            # Step 3: Determine project to use
            final_project = project_id or detected_project
            if not final_project:
                raise ValueError("No project ID available (not provided and not detected)")
            
            logger.info(f"Using project: {final_project}")
            
            # Step 4: Create client with corporate settings
            client = bigquery.Client(
                credentials=credentials,
                project=final_project,
                # Add any additional corporate-specific settings here
            )
            
            # Step 5: Test the connection
            try:
                # Simple test query to verify connection
                test_query = "SELECT 1 as test_connection"
                query_job = client.query(test_query)
                results = list(query_job.result())
                logger.info("✅ Corporate BigQuery client connection verified")
                
            except Exception as test_error:
                logger.warning(f"⚠️ Client created but connection test failed: {test_error}")
            
            return client, final_project
            
        except Exception as e:
            logger.error(f"❌ Corporate BigQuery client creation failed: {e}")
            raise

# Example usage function
def get_corporate_bigquery_client(project_id=None):
    """
    Convenience function to get a corporate BigQuery client.
    
    Args:
        project_id (str, optional): Specific project ID to use
        
    Returns:
        tuple: (client, project_id) or raises exception
    """
    config = CorporateBigQueryConfig()
    return config.create_corporate_client(project_id)

# Configuration constants you can modify for your office
CORPORATE_CONFIG = {
    # Proxy settings - modify these for your office network
    "PROXY_SETTINGS": {
        "HTTP_PROXY": "googleapis-dev.gcp.cloud.uk.hsbc:3128",
        "HTTPS_PROXY": "googleapis-dev.gcp.cloud.uk.hsbc:3128"
    },
    
    # Project patterns that indicate corporate environment
    "CORPORATE_PATTERNS": [
        'dev', 'prod', 'test', 'staging', 
        'corp', 'enterprise', 'hsbc', 'bank'
    ],
    
    # Default timeout settings for corporate networks
    "TIMEOUT_SETTINGS": {
        "query_timeout": 300,  # 5 minutes
        "connection_timeout": 60  # 1 minute
    }
}

if __name__ == "__main__":
    # Test the corporate configuration
    print("🔧 Testing Corporate BigQuery Configuration")
    print("=" * 50)
    
    try:
        config = CorporateBigQueryConfig()
        
        # Test environment detection
        is_corp = config.is_corporate_environment("test-project-dev")
        print(f"Corporate environment detected: {is_corp}")
        
        # Test proxy setup
        proxy_success = config.setup_proxy_environment()
        print(f"Proxy setup successful: {proxy_success}")
        
        print("\n✅ Corporate configuration test completed")
        
    except Exception as e:
        print(f"❌ Corporate configuration test failed: {e}")
