import pandas as pd
import os

# Find the latest Excel file
excel_files = [f for f in os.listdir('.') if f.startswith('Multi_Validation_Scenarios') and f.endswith('.xlsx')]
if excel_files:
    excel_file = sorted(excel_files)[-1]
    print(f"Using Excel file: {excel_file}")
    
    # Read all sheet names
    xl = pd.ExcelFile(excel_file)
    print(f"Available sheets: {xl.sheet_names}")
    
    # If S005 sheet exists, show its content
    if 'S005_Account_Type_Category_Validation' in xl.sheet_names:
        df = pd.read_excel(excel_file, sheet_name='S005_Account_Type_Category_Validation')
        print("S005 content:")
        print(df.to_string())
    else:
        print("S005_Account_Type_Category_Validation sheet not found!")
        # Show content of each sheet to debug
        for sheet in xl.sheet_names:
            print(f"\n--- Sheet: {sheet} ---")
            df = pd.read_excel(excel_file, sheet_name=sheet)
            print(df.to_string())
else:
    print("No Multi_Validation_Scenarios Excel files found!")
