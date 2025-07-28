from excel_handler import generate_scenarios_from_excel
import pandas as pd

# Test the Enhanced_Validation_Scenarios.xlsx
print("Testing Enhanced_Validation_Scenarios.xlsx...")
df = pd.read_excel('Enhanced_Validation_Scenarios.xlsx')
scenarios = generate_scenarios_from_excel(df, 'cohesive-apogee-411113', 'banking_sample_data')

print(f"Successfully generated {len(scenarios)} scenarios:")
for i, scenario in enumerate(scenarios, 1):
    print(f"{i}. {scenario['scenario_name']}")
    print(f"   Source: {scenario['source_table']} -> Target: {scenario['target_table']}")
    print(f"   Logic: {scenario['derivation_logic']}")
    print()

print("✅ All scenarios processed successfully!")
