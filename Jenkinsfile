pipeline {
  agent any
  stages {
    stage('Checkout'){ steps { checkout scm } }
    stage('UTCS'){ steps { sh 'python3 tools/manifest_check.py' } }
    stage('Schema'){ steps { sh 'python3 -m pip install jsonschema pyyaml && python3 - <<"PY"\nimport json, yaml, sys\nfrom jsonschema import Draft7Validator\npairs=[\n ("docs/specifications/aqua-nisq-chip.yaml","schemas/aqua-nisq-chip.schema.json"),\n ("docs/specifications/qec-lite.yaml","schemas/qec-lite.schema.json"),\n ("docs/specifications/control-plane.yaml","schemas/control-plane.schema.json"),\n ("docs/specifications/qal-backend-aqua.yaml","schemas/qal-backend-aqua.schema.json"),\n]\nok=True\nfor y,s in pairs:\n  data=yaml.safe_load(open(y))\n  schema=json.load(open(s))\n  v=Draft7Validator(schema)\n  errs=list(v.iter_errors(data))\n  if errs:\n    ok=False\n    print(f"[SCHEMA FAIL] {y}")\n    for e in errs: print(" -", e.message)\nsys.exit(0 if ok else 1)\nPY' } }
    stage('Build'){ steps { sh 'cmake -S . -B out && cmake --build out -- -j2' } }
    stage('Test'){ steps { sh './out/tests_ata27_flight_ctrl_host' } }
    stage('SAST'){ steps { sh 'cppcheck --enable=warning,style,performance,portability --error-exitcode=1 src include tests' } }
  }
}
