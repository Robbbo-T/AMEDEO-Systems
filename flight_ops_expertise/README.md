# Flight Ops Expertise (Weather • Safety • Efficiency)

Goal: Achieve 90%+ expertise across weather, safety, and efficiency for commercial flight operations using a rigorous, verifiable pipeline.

## Modules
- Data Foundations and Schema Understanding
- Feature Engineering and Representation Learning
- Supervised Multi-Task Learning and Risk Prediction
- Policy Synthesis and Best Practice Mining
- Advanced Modeling and Ensembles
- Rigorous Evaluation Protocol
- Output Synthesis and Deployment Artifacts
- Compliance, Integrity, Safety Assurance
- Operational Lifecycle Management
- Expert System Handoff and Interaction

## KPIs
- Weather: Brier ≤ 0.10, AUROC ≥ 0.92, ECE ≤ 3%
- Safety: AUROC ≥ 0.90, PR-AUC ≥ 0.35, FN ≤ 10% @ TPR=0.80
- Efficiency: MAPE(fuel) ≤ 3.0%, Policy Uplift ≥ 1.5%
- Generalization: ≤ 3% absolute gaps (manufacturer/airline holdouts)
- Robustness: Drift FAR ≤ 1%/day; calibration retained post-scaling

## Data Layout
- data/raw: source feeds (FDR/FOQA, METAR/TAF, reanalysis, schedules)
- data/processed: cleaned/parquet; train/val/test/OOD splits
- data/models: trained ckpts (weather/safety/efficiency) + calibrators
- data/artifacts: DET logs, Merkle chains, procedure cards, rule ASTs

## Dev Quickstart
1. Create and activate venv
2. Install deps
3. Run the starter notebook in notebooks/

## Acceptance Gates
W, S, E, G gates must be met for two consecutive monthly refreshes to certify 90%+ expertise.
