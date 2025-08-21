"""Mock PQC verification"""
import json
import hashlib
import argparse
import sys
from pathlib import Path


def verify_signatures(sig_file, algorithm="Dilithium3"):
    data = json.loads(Path(sig_file).read_text())
    if data.get("algorithm") != algorithm:
        print(f"❌ Algorithm mismatch: expected {algorithm}, got {data.get('algorithm')}")
        return False

    verified = 0
    failed = 0
    for file_path, sig_data in data.get("files", {}).items():
        expected_sig = hashlib.sha512(f"{algorithm}:{sig_data['hash']}:mock_key".encode()).hexdigest()[:128]
        if sig_data.get("signature") == expected_sig:
            verified += 1
        else:
            print(f"❌ Signature verification failed for {file_path}")
            failed += 1
    if failed > 0:
        return False
    return True

    print(f"✅ Verified {verified}/{len(data.get('files', {}))} signatures")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sig_file")
    parser.add_argument("--algorithm", default="Dilithium3")
    args = parser.parse_args()

    ok = verify_signatures(args.sig_file, args.algorithm)
    sys.exit(0 if ok else 1)
