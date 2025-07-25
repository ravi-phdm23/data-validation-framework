@echo off
REM Setup script for Enterprise Data Validation Framework
REM This script renames the Python files from _py to .py extension

echo ========================================
echo Enterprise Data Validation Framework
echo Setup Script for Corporate Environments
echo ========================================
echo.

echo Checking for Python files with _py extension...
echo.

if exist "data_validation_script_py" (
    echo Found: data_validation_script_py
    ren "data_validation_script_py" "data_validation_script.py"
    echo Renamed to: data_validation_script.py
    echo.
) else (
    echo Warning: data_validation_script_py not found
    echo.
)

if exist "test_bigquery_py" (
    echo Found: test_bigquery_py
    ren "test_bigquery_py" "test_bigquery.py"
    echo Renamed to: test_bigquery.py
    echo.
) else (
    echo Warning: test_bigquery_py not found
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run:
echo   python data_validation_script.py --help
echo   python test_bigquery.py
echo.
echo To install dependencies:
echo   pip install -r requirements.txt
echo.
pause
