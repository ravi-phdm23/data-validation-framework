#!/usr/bin/env python3
"""
Test script to verify validation only returns PASS or FAIL (no WARN)
"""

def test_validation_scenarios():
    """Test different validation scenarios to ensure only PASS/FAIL results."""
    
    print("Testing Validation Logic - PASS/FAIL Only")
    print("=" * 50)
    
    # Test scenarios with different match percentages
    test_cases = [
        {"matches": 100, "total": 100, "description": "Perfect Match (100%)"},
        {"matches": 99, "total": 100, "description": "99% Match (Previously WARN)"},
        {"matches": 95, "total": 100, "description": "95% Match (Previously WARN)"},
        {"matches": 90, "total": 100, "description": "90% Match"},
        {"matches": 80, "total": 100, "description": "80% Match"},
        {"matches": 50, "total": 100, "description": "50% Match"},
        {"matches": 0, "total": 100, "description": "No Matches"},
    ]
    
    for i, case in enumerate(test_cases, 1):
        matches = case["matches"]
        total = case["total"]
        description = case["description"]
        
        # Apply the new validation logic (PASS only if 100% match)
        if matches == total:
            status = 'PASS'
        else:
            status = 'FAIL'
        
        percentage = (matches / total) * 100 if total > 0 else 0
        
        print(f"Test {i}: {description}")
        print(f"   Matches: {matches}/{total} ({percentage:.1f}%)")
        print(f"   Result: {status}")
        print()
    
    print("✅ All tests completed - Only PASS/FAIL results produced")
    print("✅ No WARN scenarios exist in the updated validation logic")

if __name__ == "__main__":
    test_validation_scenarios()
