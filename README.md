# AMEDEO Systems (P0)

Unified framework for digital, environmental and operational evolution in aerospace with AQUA-OS/ADT (certifiable digital transponder).

## Scope (P0)
- Infra, CMake, CI, style configs.
- UTCS-MI v5.0 enforcement (manifest + checker + pre-commit).
- Specs (YAML + JSON Schema) with CI validation.
- Core C components: 2oo3 voter, HAL_Sim, DET stub, PQC mock, TSN sim (deterministic), POAE loop.
- ATA-27 host test: 1 kHz, 1000 steps, DET traces.
- Mermaid diagrams and minimal LaTeX (Elsevier + IEEE) built in CI.

## Build
```bash
cmake -S . -B out
cmake --build out --config Release
./out/tests_ata27_flight_ctrl_host
```

## Pre-commit hook
```bash
git config core.hooksPath .githooks
```
Hook runs: `python3 tools/manifest_check.py`

## UTCS-MI v5.0
- Canonical identifier: `EstándarUniversal:Documento-Desarrollo-DO178C-00.00-AerospaceMainEvolutionDigital-0001-v1.0-AMEDEOSystems-GeneracionHumana-CROSS-AmedeoPelliccia-7f3c9a2b-RestoDeVidaUtil`.
- Manifest at `UTCS/manifest.json` (map: path -> canonical id).
- Checker: `tools/manifest_check.py` validates identifier structure and file existence.

## CI
- GitHub Actions: `.github/workflows/ci.yml` builds, runs tests, validates UTCS and schemas, renders diagrams, builds LaTeX and publishes artifacts.
- Jenkinsfile mirrors core stages.

## Quality Gates (P0)
- UTCS: 100% artifacts listed and pass checker.
- Build: `-Wall -Wextra -Werror -O2 -pedantic` clean.
- Test: 1000 steps @1 kHz, no voter mismatches; jitter ≤ 1 ms.
- Schemas: YAML pass JSON Schema.
- SAST: cppcheck no high findings.

## Diagrams & Docs
- Mermaid sources: `docs/diagrams/*.mmd` rendered to SVG artifacts.
- LaTeX: `latex/amedeo_elsevier.tex`, `latex/main_ieee.tex`, `latex/refs.bib` built to PDFs in CI.

