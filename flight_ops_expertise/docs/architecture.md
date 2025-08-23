# System Architecture

This document outlines the high-level architecture for the Flight Operations Expertise Training System. It follows a layered lakehouse approach (Bronze → Silver → Gold) with multi-task modeling and policy synthesis.

- Data Lake: Bronze (raw), Silver (cleaned/validated), Gold (feature store)
- Modeling: Stage A (representation), Stage B (supervised multi-task)
- Synthesis: Stage C (offline RL), Stage D (best-practice mining)
- Compliance: DET provenance, S1000D DM Codes, UTCS-MI stamping
