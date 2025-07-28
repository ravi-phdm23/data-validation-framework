print("Starting test script...")

try:
    import pandas as pd
    print("Pandas imported successfully")
    
    import os
    print("OS imported successfully")
    
    from sql_generator import create_enhanced_transformation_sql
    print("SQL generator imported successfully")
    
    # Find the latest Excel file
    excel_files = [f for f in os.listdir('.') if f.startswith('Multi_Validation_Scenarios') and f.endswith('.xlsx')]
    print(f"Found {len(excel_files)} Excel files")
    
    if excel_files:
        excel_file = sorted(excel_files)[-1]
        print(f"Using Excel file: {excel_file}")
        
        # Read all scenarios from Sheet1
        df = pd.read_excel(excel_file, sheet_name='Sheet1')
        print(f"Excel file loaded with {len(df)} rows")
        
        scenarios_to_test = ['S002_Account_Balance_Validation', 'S003_Transaction_Status_Validation', 
                            'S004_Customer_Balance_Category_Validation', 'S005_Account_Type_Category_Validation']
        
        for scenario_name in scenarios_to_test:
            print(f"\n--- Testing: {scenario_name} ---")
            
            # Filter for current scenario
            scenario_df = df[df['Scenario_Name'] == scenario_name]
            
            if scenario_df.empty:
                print(f"❌ {scenario_name} not found!")
                continue
            
            try:
                # Extract configuration
                source_table = scenario_df.iloc[0]['Source_Table']
                target_table = scenario_df.iloc[0]['Target_Table']
                print(f"✅ {scenario_name}: {source_table} → {target_table}")
                
            except Exception as e:
                print(f"❌ Error with {scenario_name}: {e}")
        
        print("\nAll tests completed!")
        
    else:
        print("No Excel files found!")
        
except Exception as e:
    print(f"Fatal error: {e}")
    import traceback
    traceback.print_exc()
