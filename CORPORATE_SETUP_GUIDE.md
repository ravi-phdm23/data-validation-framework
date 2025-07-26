# Corporate BigQuery Setup Guide

## Overview
This project now supports both personal and corporate BigQuery environments. The corporate setup includes proxy configuration and alternative authentication methods suitable for office networks.

## Quick Start

### For Personal/Home Setup (Default)
```bash
python bigquery_test_scenarios.py
```

### For Corporate/Office Setup
```bash
python bigquery_test_scenarios.py --corporate
```

Or use the dedicated test script:
```bash
python test_corporate_setup.py
```

## Corporate Setup Features

### Automatic Detection
The system automatically detects corporate environments based on:
- Project ID contains 'dev', 'prod', 'test', 'staging'
- HTTP_PROXY or HTTPS_PROXY environment variables are set
- Corporate domain patterns

### Manual Override
Force corporate mode by:
1. **Command line**: `python bigquery_test_scenarios.py --corporate`
2. **Code**: `BigQueryTestScenarios(force_corporate_mode=True)`

### Proxy Configuration
The corporate setup automatically configures:
- HTTP_PROXY: `googleapis-dev.gcp.cloud.uk.hsbc:3128`
- HTTPS_PROXY: `googleapis-dev.gcp.cloud.uk.hsbc:3128`

You can modify these settings in `corporate_bigquery_config.py`.

## Testing Your Setup

### Quick Test
```bash
python test_corporate_setup.py
```

### Manual Test
```python
from bigquery_test_scenarios import BigQueryTestScenarios

# Force corporate mode
scenarios = BigQueryTestScenarios(force_corporate_mode=True)
success = scenarios.initialize_client()
print(f"Corporate setup: {'SUCCESS' if success else 'FAILED'}")
```

## Troubleshooting

### Common Issues in Corporate Environment
1. **Proxy Issues**: Verify proxy settings match your corporate network
2. **Authentication**: Run `gcloud auth application-default login`
3. **Project Access**: Ensure you have BigQuery permissions
4. **API Enabled**: Check if BigQuery API is enabled for your project

### Error Messages
- `quota exceeded`: Check project quotas and billing
- `API not enabled`: Enable BigQuery API in Google Cloud Console
- `Connection timeout`: Verify proxy settings and network access

### Getting Help
If you encounter issues:
1. Run `python test_corporate_setup.py` for detailed diagnostics
2. Check the log files generated in the project directory
3. Contact your IT support for corporate firewall/proxy configurations

## Configuration Files

- `bigquery_test_scenarios.py`: Main test scenarios with corporate support
- `corporate_bigquery_config.py`: Corporate-specific configuration
- `test_corporate_setup.py`: Corporate setup testing script
- `streamlit_app.py`: Web interface (uses auto-detection)

## Switching Between Environments

The system is designed to work seamlessly in both environments:
- **At home**: Uses standard Google Cloud authentication
- **At office**: Automatically detects corporate setup and applies proxy configuration
- **Manual override**: Use `--corporate` flag or `force_corporate_mode=True` when needed

## Examples

### Standard Usage (Auto-Detection)
```python
# This will auto-detect your environment
scenarios = BigQueryTestScenarios()
scenarios.run_all_scenarios()
```

### Force Corporate Mode
```python
# This forces corporate setup regardless of environment
scenarios = BigQueryTestScenarios(force_corporate_mode=True)
scenarios.run_all_scenarios()
```

### Custom Project with Corporate Mode
```python
# Custom project with forced corporate setup
scenarios = BigQueryTestScenarios(
    project_id="my-corporate-project-dev",
    force_corporate_mode=True
)
scenarios.run_all_scenarios()
```
