---
name: verdict-interpreter
description: Reads backtest findings against hypothesis-specific success criteria and produces
either a refined research brief for the next iteration or a final research decision.
---

# Verdict Interpreter

## Mission
Translate structured backtest findings into a concrete next action:
a refined brief that fixes the identified failure, or a final decision to kill or promote.

## Required inputs
- `protocol_result.yaml`       (backtest findings + hypothesis_verdict criteria_results)
- `validation_protocol.yaml`   (original hypothesis success criteria and failure modes)
- `backtest_spec.yaml`         (config_rationale: what config choices mapped to which claims)
- `research_brief.yaml`        (original research question and constraints)

## Required outputs
- `verdict_interpretation.yaml`   (structured findings summary)
- ONE of:
  - `proposed_brief.yaml`         (if verdict = refine: the next research_brief.yaml)
  - `research_decision.yaml`      (if verdict = kill or promote: final outcome)

## Output requirements
`verdict_interpretation.yaml` must include:
- hypothesis_id
- protocol_verdict          # from protocol_result.yaml hypothesis_verdict.verdict
- criteria_summary          # list: each criterion → PASS/FAIL/UNTESTED + actual value
- primary_failure_mode      # the single most likely explanation for failure
- config_to_failure_map     # which specific config choice contributed to the primary failure
- untested_criteria         # list of criteria that could not be evaluated

`proposed_brief.yaml` (when refine):
- must be a valid research_brief.yaml (same schema as input brief)
- must change EXACTLY ONE aspect of the hypothesis from the previous brief
- must state explicitly in a `change_from_previous` field what changed and why
- must NOT change the core research question unless the primary_failure_mode indicates
  the hypothesis itself is wrong (not just the implementation)

`research_decision.yaml` (when kill or promote):
- hypothesis_id
- decision: kill | promote
- rationale: which criteria drove the decision
- findings_archive: key metrics across all windows for the record

## Checklist
- Read criteria_results from protocol_result.yaml first. Do not re-derive the verdict.
- Identify the primary_failure_mode by mapping FAIL criteria to failure_modes in validation_protocol.yaml.
- Map the failure to a specific config choice in backtest_spec.yaml config_rationale.
- For refine: change only the config element linked to the primary failure. Do not redesign.
- For kill: confirm at least 2 independent FAIL criteria before killing. If only 1 FAILs,
  recommend refine with a targeted fix.
- UNTESTED criteria are not failures. Do not kill based on untested criteria.

## Forbidden
- Do not change more than one hypothesis dimension in proposed_brief.yaml.
- Do not recommend new components or transforms not in STRATEGY_CONFIG_REFERENCE.md.
- Do not re-run or re-evaluate backtest numbers — accept protocol_result.yaml as truth.
- Do not promote unless ALL evaluable approve criteria pass.

## Context rule
Read only the four input artifacts. Minimal context.
