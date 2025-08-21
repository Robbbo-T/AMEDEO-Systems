"""Mock PQC signing for CI/CD"""
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime


def sign_files(files, algorithm="Dilithium3", output="signatures.json"):
    signatures = {
        "algorithm": algorithm,
        "timestamp": datetime.utcnow().isoformat(),
        "files": {}
    }

    for file_path in files:
        path = Path(file_path)
        if path.exists():
            content = path.read_bytes()
            content_hash = hashlib.sha256(content).hexdigest()
            mock_signature = hashlib.sha512(f"{algorithm}:{content_hash}:mock_key".encode()).hexdigest()[:128]
            signatures["files"][str(path)] = {
                "hash": content_hash,
                "signature": mock_signature,
                "size": len(content)
            }

    Path(output).write_text(json.dumps(signatures, indent=2))
    print(f"✅ Signed {len(signatures['files'])} files with {algorithm}")
    return signatures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--algorithm", default="Dilithium3")
    parser.add_argument("--output", default="signatures.json")
    args = parser.parse_args()

    sign_files(args.files, args.algorithm, args.output)
