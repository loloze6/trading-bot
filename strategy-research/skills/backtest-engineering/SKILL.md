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
- `WORKFLOW_CAPABILITIES.md` (optional — read before emitting any config to confirm the
  required signal variant is achievable without new code. If not achievable, emit
  component_gap immediately rather than inventing a component class name.)
- `findings_carryover.yaml` (if present): read `parameter_bracket` field.
  If present, the config MUST use the midpoint value for the bracketed dimension.
  Do not use any other value. Print: "BRACKET DETECTED: {dimension} midpoint = {midpoint}"
- `run_context.yaml` (if present): read `run_type` field. See Replication guard below.

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

YAML formatting rule — applies to ALL string values in both artifacts:
- Any string value containing a colon (:) MUST use block scalar syntax (| or >) or be
  quoted with single or double quotes.
- List items (- items) that contain colons MUST be quoted: `- "key: value"` not `- key: value`
- This rule applies even inside nested mappings and multi-line values.
- Violation causes a YAML parse error that halts the pipeline.

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
- default_regime must ALWAYS be "unknown" in threshold_rules and score_product modes.
  Setting it to any active trading regime (trending, mean_reversion, chop) causes bars that
  fail the regime rules to still fire the signal — bypassing the gate entirely. This produces
  hundreds of spurious trades per window and destroys cost_drag. Always: default_regime: "unknown".
  Inactive regimes should be set to null, not to empty components lists.
- Include all regime rules from STRATEGY_CONFIG_REFERENCE.md's worked example as the
  baseline, then modify only what the hypothesis requires. Do not omit regimes not
  explicitly mentioned in the brief — omitting trending/chop means those bars fall to
  default_regime behavior.

## Replication guard
If `run_context.yaml` is present and contains `run_type: replication_diagnostic`:
- Output ONE config only. No variants (V2-V5).
- The config must exactly match `source_run`'s parameters as recorded in
  campaign_state.yaml or findings_carryover.yaml.
- Print "REPLICATION MODE: reproducing {source_run} config exactly" at the
  start of your output.
- Any deviation from source_run parameters is a critical failure of this stage.

## Forbidden
- Do not invent component classes, transform ops, or regime names absent from STRATEGY_CONFIG_REFERENCE.md.
- Do not write Python or modify the engine.
- Do not emit more than one config.
- Do not loosen any threshold or sample-split decision validation already fixed.
- Do not emit empty transforms lists unless the component's raw output is already in [-20,+20]
  and no normalization is needed. Always document why.
- NEVER set default_regime to "trending", "mean_reversion", or "chop" in threshold_rules
  or score_product mode. This is a critical config bug: it disables the regime gate and
  trades every bar. validate_config.py will reject it as VIOLATION V9. Use "unknown" only.
- Do not set default_regime to a regime that maps to null in the strategies block.
- Do not set any regime to {"components": []} (empty components list).
  If a regime should produce no trades, set it to null.
- Do not invent component class names. If you are unsure whether a variant is possible,
  read WORKFLOW_CAPABILITIES.md "Common confusion" section first. The answer is almost
  always "yes, achievable via a config parameter."

## Context rule
Read only the two hypothesis artifacts and the config reference. Minimal context.
