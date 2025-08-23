#!/usr/bin/env python3
"""
End-to-end training and synthesis pipeline for Flight Operations Expertise.
See README and configs for details.
"""
import yaml
from datetime import datetime

from src.data_ingestion.loader import load_all_sources
from src.feature_engineering.builder import build_features
from src.modeling.base_model import pretrain_representation, finetune_multi_task
from src.evaluation.metrics import evaluate_all_gates
from src.policy_synthesis.rule_miner import mine_best_practices
from src.compliance.stamping import export_wisdom_objects


def main():
    with open("configs/model_params.yml", "r") as f:
        config = yaml.safe_load(f)
    run_timestamp = datetime.utcnow().isoformat()

    raw_data, holdout_sets = load_all_sources(config['data_paths'])
    feature_store = build_features(raw_data, config['feature_params'])

    representation_model = pretrain_representation(
        feature_store.flights, config['pretrain_params']
    )

    multi_task_models = {}
    for i in range(3):
        multi_task_models[f'pipeline_{i}'] = finetune_multi_task(
            representation_model, feature_store.labels, config['finetune_params']
        )

    evaluation_results, are_gates_passed = evaluate_all_gates(
        multi_task_models, holdout_sets, config['evaluation_params']
    )

    if not all(are_gates_passed.values()):
        print("Acceptance gates not met; stopping before policy synthesis.")
        return

    best_practices = mine_best_practices(
        multi_task_models, feature_store, config['policy_params']
    )

    export_wisdom_objects(
        practices=best_practices,
        det_anchor=True,
        utcs_stamp=True,
        s1000d_dm=True,
        output_path=config['output_paths']['rule_cards'],
        run_id=run_timestamp,
    )


if __name__ == "__main__":
    main()
