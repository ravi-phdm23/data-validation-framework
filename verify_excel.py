import pandas as pd
import glob

print("=== Verification of Excel Files ===\n")

# Check Enhanced_Validation_Scenarios.xlsx
try:
    df1 = pd.read_excel('Enhanced_Validation_Scenarios.xlsx')
    print("Enhanced_Validation_Scenarios.xlsx:")
    print(f"Number of scenarios: {len(df1)}")
    print("Scenarios:")
    for i, row in df1.iterrows():
        print(f"  {i+1}. {row['Scenario_Name']}")
        print(f"     {row['Source_Table']} -> {row['Target_Table']}")
        print(f"     Logic: {row['Derivation_Logic']}")
    print()
except Exception as e:
    print(f"Error reading Enhanced_Validation_Scenarios.xlsx: {e}")

# Check Multi_Validation_Scenarios file
multi_files = glob.glob('Multi_Validation_Scenarios_*.xlsx')
if multi_files:
    try:
        df2 = pd.read_excel(multi_files[0])
        print(f"{multi_files[0]}:")
        print(f"Number of scenarios: {len(df2)}")
        print("Scenarios:")
        for i, row in df2.iterrows():
            print(f"  {i+1}. {row['Scenario_Name']}")
            print(f"     {row['Source_Table']} -> {row['Target_Table']}")
            print(f"     Type: {'Reference' if row['Reference_Table'] else 'Transformation'}")
    except Exception as e:
        print(f"Error reading {multi_files[0]}: {e}")
