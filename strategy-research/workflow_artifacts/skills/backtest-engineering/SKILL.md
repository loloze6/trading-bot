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
- `innovation_notes.yaml`  (Improvement 02: `asset_diversity_audit` candidate symbols)
- `validation_protocol.yaml`
- `COMPONENT_CATALOG.md`  (`strategy-research/docs/COMPONENT_CATALOG.md`: the inventory of every available
  component and exactly what each outputs, plus the names of every transform op, regime, and rule operator)
- `DATA_AVAILABILITY.md` (`strategy-research/docs/DATA_AVAILABILITY.md` — short, forced-read:
  what OHLCV timeframes/aux feeds are actually available, the exact-cache-missing fallback
  rule, and the bar-count/signal-shape checks to run before emitting a config for a new or
  changed timeframe. Read in full whenever the hypothesis's timeframe, symbol, or venue
  differs from what a prior config in this campaign already used.)
- `findings_carryover.yaml` (if present): read `parameter_bracket` field.
  If present, the config MUST use the midpoint value for the bracketed dimension.
  Do not use any other value. Print: "BRACKET DETECTED: {dimension} midpoint = {midpoint}"
- `run_context.yaml` (if present): read `run_type` field. See Replication guard below.

## Required outputs
- `backtest_spec.yaml`   (conforms to workflow_artifacts/schemas/backtest_spec.schema.json)
- `decision.yaml`        (conforms to workflow_artifacts/schemas/decision.schema.json)

## Output requirements
`backtest_spec.yaml`:
- `status`: "spec_ready" if a full valid config was produced, else "component_gap".
- `config`: the strategy_config object (regime_detector + strategies). Null iff status is component_gap.
- `config_rationale`: list mapping each hypothesis claim to one concrete config choice.
- `component_gap`: null when spec_ready; else {needed, kind, description}.
The embedded `config` must:
- Use ONLY components, transform ops, and regimes listed in COMPONENT_CATALOG.md. No invented names.
- Put history-based transform ops before scalar ops.
- Set explicit `lookback` on any component using ratio_to_mean / percentile / zscore.
- If `research_brief.yaml` contains a `significance_methodology` field (e.g. P1b's
  A8.5.1a mandate for backward-extension reactivation runs), copy it VERBATIM as a
  top-level key in `config` (e.g. `"significance_methodology": "episode_blocked_a851a"`).
  This is read by `protocol_execution`'s own conformance check
  (`_check_protocol_execution_conformance`, E-039 step 5) against
  `episode_blocked_significance_by_symbol` — omitting it means the pre-registered
  requirement cannot be confirmed, which would violate the brief's binding requirement.

`decision.yaml`:
- stage: "backtest_specification"
- status: same value as backtest_spec.status (spec_ready | component_gap)
- rationale: one line on why
- blocking_issues: the missing piece(s) if component_gap, else []

## IMPROVEMENT 01 — Name the Chosen Variant (E-034 S2)

`expanded_hypothesis_card.yaml`'s `expanded_variants` list is a menu, sometimes several
entries wide. You pick exactly one to turn into `config` (per the Forbidden rule below:
"Do not emit more than one config"). Downstream code needs to know mechanically which
menu entry that was — not by grepping your prose.

**When `status: "spec_ready"`, `backtest_spec.yaml` MUST include a top-level
`selected_variant_id` field**, copied verbatim from the `expanded_variants` entry you
implemented:
- If the entry is a dict with a `variant_id` key, copy that value verbatim.
- If it is a dict without `variant_id` but with `id`, `name`, `variant_name`, or `label`,
  copy the first of those present, in that order.
- If it is a bare string, copy the string itself verbatim.

Pick from the closed set already in front of you in `expanded_hypothesis_card.yaml` — do
not invent an ID, and do not synthesize a hybrid of two menu entries and label it as one
of them. **If no single menu entry is a full, honest match for the config you would
otherwise write, that is a component_gap, exactly like a missing engine piece**: set
`status: "component_gap"`, leave `config: null`, and describe in `component_gap` why
none of the offered variants map cleanly. Do not silently pick the closest one and call
it a match.

`selected_variant_id` is read by deterministic code immediately after this stage
completes, joined against the same menu — it is a closed-set, machine-checked pick, the
same shape as `status` itself, not a free-text field. **Required outputs, updated:**
`backtest_spec.yaml` MUST include `selected_variant_id` (string) whenever
`status: "spec_ready"`.

YAML formatting rule — applies to ALL string values in both artifacts:
- Any string value containing a colon (:) MUST use block scalar syntax (| or >) or be
  quoted with single or double quotes.
- List items (- items) that contain colons MUST be quoted: `- "key: value"` not `- key: value`
- This rule applies even inside nested mappings and multi-line values.
- Violation causes a YAML parse error that halts the pipeline.

## IMPROVEMENT 02 — Asset generalizability carries through from innovation_expansion (E-026, 2026-09-12)

`innovation_notes.yaml`'s `asset_diversity_audit` (Improvement 06 of that
stage) names the candidate symbols this hypothesis should also be tested
against, from a DIFFERENT `config/coin_universe.yaml` category than the base
instrument — unless it carries an explicit single-asset opt-out. Whatever
protocol/symbol set this run ends up targeting (pinned, generated, or
inherited — see the four branches in `_resolve_protocol_path`) should include
those candidates alongside the base instrument, not the base instrument
alone, UNLESS:
- `run_context.yaml` marks this a `replication_diagnostic` (Replication guard
  above already forbids any deviation from `source_run` there — this rule
  never overrides that), or
- `asset_diversity_audit.opt_out` is non-null (a genuinely single-asset
  mechanism), or
- `machine_constraints.protocol_ref` pins a specific pre-existing protocol
  (a pinned protocol's own symbol set is what it is — do not silently expand
  a protocol someone else already fixed).

If none of those apply and the resolved protocol still only covers the base
instrument's own category, say so plainly in `decision.yaml`'s `rationale`
rather than silently proceeding — this is the same "don't skip it quietly"
discipline Improvement 06 applies one stage earlier.

## Required prerequisite reading
Read workflow_artifacts/skills/quant-fundamentals/SKILL.md before proposing any config change justified
by a metric value (e.g. raising/lowering a threshold because of cost_drag or corr).
If a stated rationale conflicts with an identity in quant-fundamentals,
quant-fundamentals is authoritative — note the conflict rather than silently following
the original rationale.

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
- default_regime must be "unknown" in threshold_rules and score_product modes WHENEVER
  regime_detector.rules is non-empty (a real gate exists). Setting it to trending,
  mean_reversion, or chop in that case causes bars that fail every rule to still fire
  the signal — bypassing the gate entirely. This produces hundreds of spurious trades
  per window and destroys cost_drag. `validate_config.py` VIOLATION V9 enforces this
  for all three names (trending/mean_reversion/chop), not just trending.
  **This restriction does NOT apply to the fully-ungated pattern** (regime_detector.rules=[]
  AND regime_detector.components=[]) — see "Ungated hypotheses" below; there any of the
  four names is accepted (`"unknown"` by convention).
- Write every regime rule against a measure from the "Regime measures" rows of COMPONENT_CATALOG.md (its
  range and sign say where a threshold can sit), then modify only what the hypothesis requires. Do not omit
  regimes not explicitly mentioned in the brief — omitting trending/chop means those bars fall to
  default_regime behavior.

## Ungated hypotheses (post-A2.3) — THE canonical pattern

A2.3 standing policy: the BTC/ETH 1h regime detector is unusable, so most hypotheses in
this campaign are ungated (no regime condition at all — the signal is meant to be active
on every bar). Building this incorrectly is what caused run_043's first blocker
(2026-07-04): a dummy always-true rule targeting an invented regime name ("active",
outside the four-value enum), rejected by VIOLATION V7.

**Use exactly this pattern — verified empirically against the live engine, not by
reasoning about it (see `trading-bot/tests/test_ungated_config_pattern.py`):**

```json
"regime_detector": {
  "mode": "threshold_rules",
  "components": [],
  "rules": [],
  "default_regime": "unknown"
},
"strategies": {
  "warmup": <N>,
  "regimes": {
    "unknown": { "components": [ /* the real signal */ ] },
    "trending": null, "mean_reversion": null, "chop": null
  }
}
```

- `regime_detector.rules=[]` and `components=[]`: `ConfigDrivenRegimeEngine
  ._classify_threshold_rules()` has no rule to walk and no component to read, so it
  falls straight through to `default_regime` on every single bar, unconditionally.
  No dummy component, no always-true rule — those add moving parts for zero benefit
  and are what produced the invented-name failure.
- **`default_regime`: any of the four names is accepted here; use `"unknown"` by convention.** With no rules
  and no components every bar resolves to `default_regime`, so it is a label, not a gate: what matters is that
  `strategies.regimes[default_regime]` holds the real signal (next bullet). All four labels give the same
  forecasts from the first ready bar on (`trading-bot/tests/test_ungated_config_pattern.py`,
  `test_pattern_a_all_four_regime_labels_now_agree`).
- `validate_config.py` VIOLATION V10 enforces the concrete authoring mistake this pattern
  invites: if `regime_detector.components=[]` and `rules=[]`, `strategies.regimes
  [default_regime]` must not be null — that combination is silently dead (forecasts 0.0
  forever) with no error anywhere else to catch it.

## Replication guard
If `run_context.yaml` is present and contains `run_type: replication_diagnostic`:
- Output ONE config only. No variants (V2-V5).
- The config must exactly match `source_run`'s parameters as recorded in
  campaign_state.yaml or findings_carryover.yaml.
- Print "REPLICATION MODE: reproducing {source_run} config exactly" at the
  start of your output.
- Any deviation from source_run parameters is a critical failure of this stage.

## Forbidden
- Do not invent component classes, transform ops, or regime names absent from COMPONENT_CATALOG.md.
- Do not write Python or modify the engine.
- Do not emit more than one config.
- Do not loosen any threshold or sample-split decision validation already fixed.
- Do not emit empty transforms lists unless the component's raw output is already in [-20,+20]
  and no normalization is needed. Always document why.
- NEVER set default_regime to "trending", "mean_reversion", or "chop" in threshold_rules
  or score_product mode WHILE regime_detector.rules is non-empty. This is a critical
  config bug: it disables the regime gate and trades every bar. validate_config.py will
  reject it as VIOLATION V9. Use "unknown" whenever rules is non-empty.
  (For a fully-ungated config — rules=[] AND components=[] — this restriction does not
  apply; see "Ungated hypotheses" above: any of the four names is accepted there, `"unknown"`
  by convention, as long as it points at a regime that holds the signal.)
- Do not set default_regime to a regime that maps to null in the strategies block.
- Do not set any regime to {"components": []} (empty components list).
  If a regime should produce no trades, set it to null.
- Do not invent component class names. If you are unsure whether a variant is possible,
  read the component's row and the "Variant patterns" section of COMPONENT_CATALOG.md first. The answer is almost
  always "yes, achievable via a config parameter."

## Context rule
Read only the hypothesis artifacts (including `innovation_notes.yaml` for
Improvement 02) and the config reference. Minimal context.
