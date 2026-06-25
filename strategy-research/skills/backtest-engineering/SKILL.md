---
name: backtest-engineering
description: Converts an approved, validated trading hypothesis into a concrete strategy_config candidate for the config-driven backtest engine, or flags that a required engine component does not yet exist.
---

# Backtest Engineering

## Mission
Translate the approved hypothesis into one valid strategy config (emitted inside `backtest_spec.yaml` under
`config`) for the config-driven engine — OR declare a component gap if the engine lacks a required piece.

## Required inputs
- `expanded_hypothesis_card.yaml`
- `validation_protocol.yaml`
- `STRATEGY_CONFIG_REFERENCE.md`  (trading-bot config reference: the authoritative list of every available
  component, transform op, regime, and parameter)

## Required outputs
- `backtest_spec.yaml`   (conforms to schemas/backtest_spec.schema.json)
- `decision.yaml`        (conforms to schemas/decision.schema.json)

## Output requirements
`backtest_spec.yaml`:
- `status`: "spec_ready" if a full valid config was produced, else "component_gap".
- `config`: the strategy_config object (regime_detector + strategies). Null iff status is component_gap.
- `config_rationale`: list mapping each hypothesis claim to one concrete config choice.
- `component_gap`: null when spec_ready; else {needed, kind, description}.
The embedded `config` must:
- Use ONLY components, transform ops, and regimes listed in STRATEGY_CONFIG_REFERENCE.md. No invented names.
- Put history-based transform ops before scalar ops.
- Set explicit `lookback` on any component using ratio_to_mean / percentile / zscore.

`decision.yaml`:
- stage: "backtest_specification"
- status: same value as backtest_spec.status (spec_ready | component_gap)
- rationale: one line on why
- blocking_issues: the missing piece(s) if component_gap, else []

## Checklist
- In config_rationale, show how the signal concept becomes component + transform pipeline.
- Pick regime mode the hypothesis needs; default threshold_rules. One active regime is fine for a first test.
- Keep the config minimal.
- If ANY required indicator/transform/regime is absent from the reference, status=component_gap; do not
  fabricate a config around the missing piece.

## Forbidden
- Do not invent component classes, transform ops, or regime names absent from STRATEGY_CONFIG_REFERENCE.md.
- Do not write Python or modify the engine.
- Do not emit more than one config.
- Do not loosen any threshold or sample-split decision validation already fixed.

## Context rule
Read only the two hypothesis artifacts and the config reference. Minimal context.
