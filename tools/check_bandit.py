"""Check bandit results for HIGH severity issues"""
import json
import sys
from pathlib import Path


def check_bandit_results(bandit_file: str) -> bool:
    p = Path(bandit_file)
    if not p.exists():
        print(f"❌ Bandit output not found: {bandit_file}")
        return False
    results = json.loads(p.read_text())
    if high := [
        r
        for r in results.get("results", [])
        if r.get("issue_severity") == "HIGH"
    ]:
        print("❌ HIGH severity security issues found:")
        for issue in high:
            print(f"   - {issue['filename']}:{issue['line_number']} - {issue['test_name']}")
        return False
    print("✅ No HIGH severity security issues found")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/check_bandit.py <bandit_results.json>")
        sys.exit(1)
    ok = check_bandit_results(sys.argv[1])
    sys.exit(0 if ok else 1)
