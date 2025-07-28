#!/usr/bin/env python3
"""
Test script to debug the validation scenario execution
"""

import pandas as pd
from bigquery_client import connect_to_bigquery, execute_custom_query
from excel_handler import generate_scenarios_from_excel

def test_scenario():
    """Test the specific scenario that's failing"""
    
    print("Testing BigQuery connection...")
    try:
        client = connect_to_bigquery('cohesive-apogee-411113', 'banking_sample_data')
        if client:
            print("✅ BigQuery connection successful")
        else:
            print("❌ BigQuery connection failed")
            return
    except Exception as e:
        print(f"❌ BigQuery connection error: {e}")
        return
    
    print("\nReading Excel scenario...")
    try:
        df = pd.read_excel('S001_Customer_Name_Validation.xlsx')
        
        print("Scenario details:")
        for col in df.columns:
            print(f"  {col}: {df.iloc[0][col]}")
        
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return
    
    print("\nGenerating scenarios from Excel...")
    try:
        scenarios = generate_scenarios_from_excel(
            df, 
            'cohesive-apogee-411113', 
            'banking_sample_data'
        )
        
        if scenarios:
            print(f"✅ Generated {len(scenarios)} scenario(s)")
            scenario = scenarios[0]
            print("\nScenario structure:")
            for key, value in scenario.items():
                print(f"  {key}: {value}")
        else:
            print("❌ No scenarios generated")
            return
            
    except Exception as e:
        print(f"❌ Error generating scenarios: {e}")
        import traceback
        print(traceback.format_exc())
        return
    
    print("\nTesting scenario execution...")
    try:
        from excel_handler import execute_all_excel_scenarios
        from streamlit import session_state
        
        # Mock session state
        class MockSessionState:
            def __init__(self):
                self.excel_scenarios = scenarios
        
        # Temporarily set up mock session state
        import streamlit as st
        if not hasattr(st, 'session_state'):
            st.session_state = MockSessionState()
        else:
            st.session_state.excel_scenarios = scenarios
        
        results = execute_all_excel_scenarios()
        
        print(f"✅ Execution completed")
        print(f"   Results: {len(results) if results else 0} scenario(s)")
        
        if results:
            for result in results:
                print(f"\nScenario: {result.get('scenario_name', 'Unknown')}")
                print(f"  Status: {result.get('status', 'Unknown')}")
                if result.get('error_message'):
                    print(f"  Error: {result['error_message']}")
                else:
                    print(f"  Total Records: {result.get('total_records', 0)}")
                    print(f"  Passed Records: {result.get('passed_records', 0)}")
            
    except Exception as e:
        print(f"❌ Error executing scenarios: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_scenario()
