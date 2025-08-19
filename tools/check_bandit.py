"""Security scan validation for Bandit"""
import json
import sys
from pathlib import Path

def check_bandit_results(bandit_file):
    """Check bandit results and fail on HIGH severity issues."""
    
    if not Path(bandit_file).exists():
        print(f"❌ Bandit results file not found: {bandit_file}")
        sys.exit(1)
    
    try:
        with open(bandit_file) as f:
            results = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in bandit results: {e}")
        sys.exit(1)
    
    high_issues = []
    total_issues = 0
    
    for result in results.get("results", []):
        severity = result.get("issue_severity", "").upper()
        total_issues += 1
        
        if severity == "HIGH":
            high_issues.append({
                "file": result.get("filename", "unknown"),
                "line": result.get("line_number", 0),
                "test": result.get("test_name", "unknown"),
                "message": result.get("issue_text", "No message")
            })
    
    print(f"📊 Bandit scan results: {total_issues} total issues")
    
    if high_issues:
        print(f"❌ Found {len(high_issues)} HIGH severity security issues:")
        for issue in high_issues:
            print(f"   {issue['file']}:{issue['line']} - {issue['test']}")
            print(f"      {issue['message']}")
        sys.exit(1)
    else:
        print("✅ No HIGH severity security issues found")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_bandit.py <bandit_results.json>")
        sys.exit(1)
    
    check_bandit_results(sys.argv[1])