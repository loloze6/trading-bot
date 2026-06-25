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
- transforms list must not be empty for directional signal components. If no normalization
  is intended, include {"op": "identity"} explicitly to confirm intent.
- scaling_factor and transform pipeline interact: if using ratio_to_mean + scale,
  scaling_factor controls raw signal range before normalization; if transforms is empty,
  scaling_factor IS the forecast magnitude — ensure it produces values in [-20, +20].
- default_regime must map to a regime with at least one component with weight > 0. The
  correct default for a hypothesis with one active regime is to set default_regime to that
  active regime (e.g. mean_reversion). Inactive regimes should be set to null, not to
  empty components lists.
- Include all regime rules from STRATEGY_CONFIG_REFERENCE.md's worked example as the
  baseline, then modify only what the hypothesis requires. Do not omit regimes not
  explicitly mentioned in the brief — omitting trending/chop means those bars fall to
  default_regime behavior.

## Forbidden
- Do not invent component classes, transform ops, or regime names absent from STRATEGY_CONFIG_REFERENCE.md.
- Do not write Python or modify the engine.
- Do not emit more than one config.
- Do not loosen any threshold or sample-split decision validation already fixed.
- Do not emit empty transforms lists unless the component's raw output is already in [-20,+20]
  and no normalization is needed. Always document why.
- Do not set default_regime to a regime that maps to null in the strategies block.
- Do not set any regime to {"components": []} (empty components list).
  If a regime should produce no trades, set it to null.

## Context rule
Read only the two hypothesis artifacts and the config reference. Minimal context.
