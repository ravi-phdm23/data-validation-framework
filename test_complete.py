#!/usr/bin/env python3
"""
Test the complete validation workflow
"""

import pandas as pd
import streamlit as st
from excel_handler import generate_scenarios_from_excel, execute_all_excel_scenarios

def test_complete_workflow():
    """Test the complete validation workflow"""
    
    print("Testing complete validation workflow...")
    
    # Read the Excel file
    df = pd.read_excel('S001_Customer_Name_Validation.xlsx')
    
    # Generate scenarios
    scenarios = generate_scenarios_from_excel(df, 'cohesive-apogee-411113', 'banking_sample_data')
    
    if not scenarios:
        print("❌ No scenarios generated")
        return
    
    print(f"✅ Generated {len(scenarios)} scenario(s)")
    scenario = scenarios[0]
    
    # Check the scenario details
    print(f"\nScenario details:")
    print(f"  Name: {scenario['scenario_name']}")
    print(f"  Source table: {scenario['source_table']}")
    print(f"  Target table: {scenario['target_table']}")
    print(f"  Reference table: '{scenario['reference_table']}'")
    print(f"  Reference table check: {str(scenario['reference_table']).lower() not in ['nan', 'none', '']}")
    print(f"  Target table check: {str(scenario['target_table']).lower() not in ['nan', 'none', '']}")
    
    # Mock the streamlit session state
    class MockSessionState:
        def __init__(self):
            self.data = {}
        
        def __getitem__(self, key):
            return self.data[key]
        
        def __setitem__(self, key, value):
            self.data[key] = value
        
        def __contains__(self, key):
            return key in self.data
        
        def get(self, key, default=None):
            return self.data.get(key, default)
    
    # Set up mock session state
    st.session_state = MockSessionState()
    st.session_state['excel_scenarios'] = scenarios
    
    # Mock streamlit functions
    class MockProgress:
        def __init__(self, total):
            self.total = total
            self.current = 0
        
        def progress(self, value):
            self.current = value
            print(f"Progress: {int(value * 100)}%")
    
    class MockEmpty:
        def text(self, text):
            print(f"Status: {text}")
    
    # Patch streamlit functions
    original_progress = st.progress
    original_empty = st.empty
    original_error = st.error
    original_success = st.success
    
    st.progress = lambda x: MockProgress(1)
    st.empty = lambda: MockEmpty()
    st.error = lambda x: print(f"ERROR: {x}")
    st.success = lambda x: print(f"SUCCESS: {x}")
    
    try:
        # Execute scenarios
        results = execute_all_excel_scenarios()
        
        if results:
            print(f"\n✅ Execution completed with {len(results)} result(s)")
            
            for result in results:
                print(f"\nResult for: {result.get('scenario_name', 'Unknown')}")
                print(f"  Status: {result.get('status', 'Unknown')}")
                if result.get('error_message'):
                    print(f"  Error: {result['error_message']}")
                else:
                    print(f"  Total Records: {result.get('total_records', 0)}")
                    print(f"  Passed Records: {result.get('passed_records', 0)}")
                    if result.get('result_data') is not None:
                        df_result = result['result_data']
                        if not df_result.empty:
                            print(f"  Sample data: {df_result.iloc[0].to_dict()}")
        else:
            print("❌ No results returned")
            
    finally:
        # Restore original functions
        st.progress = original_progress
        st.empty = original_empty
        st.error = original_error
        st.success = original_success

if __name__ == "__main__":
    test_complete_workflow()
