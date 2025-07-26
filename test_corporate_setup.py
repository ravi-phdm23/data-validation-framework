#!/usr/bin/env python3
"""
Corporate Setup Test Script
Use this script to test BigQuery connectivity in your office environment
"""

import os
import sys
from datetime import datetime
from bigquery_test_scenarios import BigQueryTestScenarios

def test_corporate_setup():
    """Test BigQuery connection using corporate setup."""
    
    print("🏢 Testing Corporate BigQuery Setup")
    print("=" * 50)
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test 1: Force corporate mode
    print("\n📋 Test 1: Forced Corporate Mode")
    try:
        test_scenarios = BigQueryTestScenarios(
            project_id="cohesive-apogee-411113", 
            force_corporate_mode=True  # This forces corporate setup
        )
        
        success = test_scenarios.initialize_client()
        if success:
            print("✅ Corporate mode initialization: SUCCESS")
            
            # Try a simple query
            query = "SELECT 1 as test_value, 'Corporate Setup Working' as message"
            results = test_scenarios.execute_query(query, "Corporate Setup Test")
            
            if results:
                print("✅ Corporate query execution: SUCCESS")
                for row in results:
                    print(f"   Result: {row.test_value} - {row.message}")
            else:
                print("❌ Corporate query execution: FAILED")
        else:
            print("❌ Corporate mode initialization: FAILED")
            
    except Exception as e:
        print(f"❌ Corporate test failed: {e}")
    
    # Test 2: Auto-detection mode (current default)
    print("\n📋 Test 2: Auto-Detection Mode")
    try:
        test_scenarios = BigQueryTestScenarios(project_id="cohesive-apogee-411113")
        
        success = test_scenarios.initialize_client()
        if success:
            print("✅ Auto-detection initialization: SUCCESS")
        else:
            print("❌ Auto-detection initialization: FAILED")
            
    except Exception as e:
        print(f"❌ Auto-detection test failed: {e}")
    
    # Test 3: Check environment variables
    print("\n📋 Test 3: Environment Check")
    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY"]
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set")
    
    # Test 4: Network connectivity hint
    print("\n📋 Test 4: Network Connectivity Hints")
    print("💡 If tests fail in corporate environment:")
    print("   - Verify proxy settings: googleapis-dev.gcp.cloud.uk.hsbc:3128")
    print("   - Check if BigQuery API is enabled for your project")
    print("   - Ensure you have proper authentication (gcloud auth list)")
    print("   - Contact IT support for corporate firewall rules")
    
    print("\n🎯 Corporate Setup Test Completed")

def main():
    """Main function."""
    try:
        test_corporate_setup()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test script failed: {e}")

if __name__ == "__main__":
    main()
