#!/usr/bin/env python3
"""
Deployment Package Creator for BigQuery Data Validation Framework
Creates deployment packages with essential files for production use.
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_deployment_package(package_type="complete"):
    """Create deployment package with essential files."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Define file lists for different deployment types
    essential_files = [
        'streamlit_app.py',
        'requirements.txt', 
        'BigQuery_Test_Scenarios_Sample.xlsx',
        'README.md'
    ]
    
    recommended_files = [
        'test_all_scenarios.py',
        'generate_sample_data.py',
        'upload_csv_to_bigquery.py',
        'DEPLOYMENT_SUCCESS_SUMMARY.md',
        'DEPLOYMENT_FILE_LIST.md'
    ]
    
    optional_files = [
        'STREAMLIT_USER_GUIDE.md',
        'CORPORATE_SETUP_GUIDE.md',
        'debug_scenario.py'
    ]
    
    # Select files based on package type
    if package_type == "minimal":
        files_to_include = essential_files
        package_name = f"bigquery_validation_minimal_{timestamp}"
    elif package_type == "complete":
        files_to_include = essential_files + recommended_files
        package_name = f"bigquery_validation_complete_{timestamp}"
    elif package_type == "full":
        files_to_include = essential_files + recommended_files + optional_files
        package_name = f"bigquery_validation_full_{timestamp}"
    else:
        files_to_include = essential_files
        package_name = f"bigquery_validation_custom_{timestamp}"
    
    # Create package directory
    package_dir = f"./{package_name}"
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy files to package directory
    copied_files = []
    missing_files = []
    
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            copied_files.append(file)
            print(f"✅ Copied: {file}")
        else:
            missing_files.append(file)
            print(f"❌ Missing: {file}")
    
    # Create deployment instructions
    instructions = f"""# BigQuery Data Validation Framework - Deployment Package
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Package Type: {package_type.upper()}

## Files Included ({len(copied_files)} files):
{chr(10).join([f"- {file}" for file in copied_files])}

## Quick Start:
1. Install dependencies: `pip install -r requirements.txt`
2. Setup Google Cloud: `gcloud auth application-default login`
3. Run application: `streamlit run streamlit_app.py --server.port 8502`
4. Open browser: http://localhost:8502

## Verification:
- Run test script: `python test_all_scenarios.py` (if included)
- Expected result: 8/8 scenarios PASS

## Support:
- Repository: https://github.com/ravi-phdm23/data-validation-framework
- Status: Production Ready ✅
"""
    
    # Write instructions to package
    with open(f"{package_dir}/DEPLOYMENT_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    
    # Create ZIP package
    zip_filename = f"{package_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    # Calculate package size
    package_size = os.path.getsize(zip_filename) / 1024  # KB
    
    # Summary
    print(f"\n🎉 DEPLOYMENT PACKAGE CREATED SUCCESSFULLY")
    print(f"📦 Package: {zip_filename}")
    print(f"📁 Directory: {package_dir}/")
    print(f"📊 Size: {package_size:.1f} KB")
    print(f"📋 Files: {len(copied_files)} included")
    
    if missing_files:
        print(f"⚠️  Missing files: {len(missing_files)}")
        for file in missing_files:
            print(f"   - {file}")
    
    print(f"\n✅ Ready for deployment!")
    print(f"📤 Send {zip_filename} to end users")
    print(f"📖 Instructions included in package")
    
    return zip_filename, package_dir

def main():
    """Main function to create deployment packages."""
    print("🚀 BigQuery Data Validation Framework - Deployment Package Creator")
    print("=" * 70)
    
    # Create different package types
    packages_created = []
    
    # 1. Minimal package (4 essential files)
    print("\n📦 Creating MINIMAL deployment package...")
    try:
        zip_file, package_dir = create_deployment_package("minimal")
        packages_created.append(("Minimal", zip_file))
    except Exception as e:
        print(f"❌ Error creating minimal package: {e}")
    
    # 2. Complete package (8 recommended files)
    print("\n📦 Creating COMPLETE deployment package...")
    try:
        zip_file, package_dir = create_deployment_package("complete")
        packages_created.append(("Complete", zip_file))
    except Exception as e:
        print(f"❌ Error creating complete package: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 DEPLOYMENT PACKAGES SUMMARY")
    print("=" * 70)
    
    for package_type, zip_file in packages_created:
        if os.path.exists(zip_file):
            size = os.path.getsize(zip_file) / 1024
            print(f"✅ {package_type:10} | {zip_file:40} | {size:6.1f} KB")
        else:
            print(f"❌ {package_type:10} | Package creation failed")
    
    print(f"\n🚀 Total packages created: {len(packages_created)}")
    print(f"📤 Ready for distribution to end users!")
    
    if packages_created:
        print(f"\n📋 DISTRIBUTION INSTRUCTIONS:")
        print(f"1. Send ZIP files to end users")
        print(f"2. Users extract and follow DEPLOYMENT_INSTRUCTIONS.txt")
        print(f"3. Expected result: 100% working BigQuery validation system")

if __name__ == "__main__":
    main()
