---
name: strategy-config-authoring
description: Converts an approved hypothesis directly into one base strategy_config candidate for the config-driven backtest engine, BEFORE variant expansion -- or flags that a required engine component does not yet exist. Config-direct-authoring path only (orchestrator.config_direct_authoring.enabled); adapted from backtest-engineering/SKILL.md, relocated from post-validation (~5) to pre-expansion (1b).
---

# Strategy Config Authoring

## Mission
Translate the approved hypothesis into one valid BASE strategy config (emitted inside `backtest_spec.yaml` under
`config`) for the config-driven engine — OR declare a component gap if the engine lacks a required piece.

**Where this stage sits (config-direct-authoring flow only, `orchestrator.config_direct_authoring.enabled: true`):**
`hypothesis_generation` → **`strategy_config_authoring` (this skill)** → `innovation_expansion` →
`backtest_specification` (tool-only; applies `innovation_expansion`'s patches to the base config this stage
produces). This is the reverse of the flag-off order, where `backtest-engineering` (the skill this file is
adapted from) runs AFTER `innovation_expansion` and picks one variant from an already-expanded menu. Here, no
variant menu exists yet — this stage authors the single BASE config; `innovation_expansion` (rewritten for this
flow) is what turns it into variants, expressed as patches against the config this stage writes.

## Required inputs
- `hypothesis_card.yaml` (the base hypothesis — NOT `expanded_hypothesis_card.yaml`; no variant menu exists at
  this point in the config-direct-authoring flow)
- `STRATEGY_DESIGN_GUIDE.md` (`strategy-research/docs/STRATEGY_DESIGN_GUIDE.md` — how to design a config for THIS
  flow: how a config becomes a trade, the graded-forecast rule, every key and option, the transform ops, how to
  compose a signal, what the config cannot express, the validator rules, and the `block_manifest.yaml` contract
  you write, see Output requirements.)
- `COMPONENT_CATALOG.md` (`strategy-research/docs/COMPONENT_CATALOG.md` — the inventory of every available
  component and exactly what each outputs: formula, range and sign, graded or on/off, warmup, data needs.)
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
- `backtest_spec.yaml`   (same artifact name and shape `backtest-engineering` uses, minus `selected_variant_id`
  — see IMPROVEMENT 01's removal note below)
- `decision.yaml`        (conforms to workflow_artifacts/schemas/decision.schema.json)
- `block_manifest.yaml`  (only when status is spec_ready; STRATEGY_DESIGN_GUIDE.md 'Manifest contract' — see below)

## Output requirements
`backtest_spec.yaml`:
- `status`: "spec_ready" if a full valid config was produced, else "component_gap".
- `config`: the strategy_config object (regime_detector + strategies). Null iff status is component_gap.
- `config_rationale`: list mapping each hypothesis claim to one concrete config choice.
- `component_gap`: null when spec_ready; else {needed, kind, description}.
The embedded `config` must:
- Use ONLY components listed in COMPONENT_CATALOG.md, and transform ops and regimes listed in
  STRATEGY_DESIGN_GUIDE.md. No invented names.
- Put history-based transform ops before scalar ops.
- Set explicit `lookback` on any component using ratio_to_mean / percentile / zscore.
- If `research_brief.yaml` contains a `significance_methodology` field (e.g. P1b's
  A8.5.1a mandate for backward-extension reactivation runs), copy it VERBATIM as a
  top-level key in `config` (e.g. `"significance_methodology": "episode_blocked_a851a"`).
  This is read by `protocol_execution`'s own conformance check
  (`_check_protocol_execution_conformance`, E-039 step 5) against
  `episode_blocked_significance_by_symbol` — omitting it means the pre-registered
  requirement cannot be confirmed, which would violate the brief's binding requirement.

`block_manifest.yaml` (next to `backtest_spec.yaml`; write it only when status is spec_ready). It says which
part of the config you just wrote IS the hypothesis's block and which part is scaffolding. Exact shape, every key
required, no other key (STRATEGY_DESIGN_GUIDE.md 'Manifest contract'):
```yaml
block:
  kind: forecast            # forecast | regime -- nothing else
  config_paths:             # JSON pointers into `config` (NOT into backtest_spec.yaml), e.g.
    - /strategies/regimes/unknown/components/0
scaffolding:                # JSON pointers to config the idea needs but that is not the idea; may be []
  - /strategies/warmup
  - /regime_detector
rationale: one or two sentences -- which hypothesis claim each block path implements
```
- `kind: forecast` when the idea is a signal: at least one `config_paths` entry inside a named regime
  (`/strategies/regimes/<name>/...`; the bare `/strategies/regimes` does not count).
  `kind: regime` when the idea is a regime gate: at least one entry at or under `/regime_detector`.
- Every pointer must exist in `config`. A piece is block or scaffolding, never both: no pointer may sit inside
  another's subtree. The orchestrator checks all of this right after this stage: one miss sends you back once
  with the error, a second stops the run.
- No symbol/coin/timeframe field and no hypothesis id — a validated block is usable on any coin, and the run
  already carries its `hypothesis_id`.

`decision.yaml`:
- stage: "strategy_config_authoring"
- status: same value as backtest_spec.status (spec_ready | component_gap)
- rationale: one line on why
- blocking_issues: the missing piece(s) if component_gap, else []

## Pass-through candidates (hypothesis-design IMPROVEMENT 08)

If `hypothesis_card.yaml` carries `pass_through: true`, its `config` field is already a complete,
upstream-authored strategy config (see `hypothesis-design/SKILL.md`'s IMPROVEMENT 08). Copy it through verbatim
as this stage's own `backtest_spec.yaml.config`, and its `manifest` field verbatim as `block_manifest.yaml` —
do not re-author, re-derive `config_rationale` from scratch
(state "pass-through, see hypothesis_card.yaml.rationale" instead), or second-guess the supplied config's
component choices. Still run it through the same validation this stage always performs before emitting
`status: spec_ready` — a pass-through config is not exempt from being a VALID config, only from being
re-invented.

## IMPROVEMENT 01 — Name the Chosen Variant: REMOVED for this flow

`backtest-engineering/SKILL.md`'s own IMPROVEMENT 01 required a `selected_variant_id` field, picked from
`expanded_hypothesis_card.yaml`'s already-expanded `expanded_variants` menu. **That menu does not exist yet at
this point in the config-direct-authoring flow** — `innovation_expansion` runs AFTER this stage, not before it,
and produces `variant_patches.yaml` (patches against the config THIS stage writes), not a prose menu this stage
would pick one entry from. There is nothing to select here: this stage always authors exactly one base config.
Do not emit a `selected_variant_id` field in `backtest_spec.yaml` — it has no menu to be a closed-set pick
against in this flow, and `_record_variant_selection`'s own flag
(`orchestrator.variant_selection_record.enabled`) is a different, older single-selected-variant mechanism this
flow does not use (config-direct authoring produces N pursued variants per run via
`innovation_expansion`'s patches downstream, not one selected-vs-discarded choice here).

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
  AND regime_detector.components=[]) — see "Ungated hypotheses" below; that is a
  different, separately-canonical case with its own rule.
- Include all regime rules from STRATEGY_DESIGN_GUIDE.md's worked example as the
  baseline, then modify only what the hypothesis requires. Do not omit regimes not
  explicitly mentioned in the brief — omitting trending/chop means those bars fall to
  default_regime behavior.
- Write `block_manifest.yaml` for every spec_ready config (see Output requirements). Do not invent a
  symbol/timeframe/instrument-set config field — the config has none (STRATEGY_DESIGN_GUIDE.md
  'What the config cannot express').

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
- **`default_regime` MUST be `"unknown"` here — not "any of the four, pick one."**
  Empirically confirmed: `main_strategy.is_ready()` gates on
  `strategy_engine.is_ready(self.regime_engine.current_regime)`, read BEFORE
  `classify()` has run for the current bar — so on the very first ready-candidate bar,
  `current_regime` is still its class-initial default, `MarketRegime.UNKNOWN`, no matter
  what the config's real target is. `ConfigDrivenStrategyEngine.is_ready()` returns True
  UNCONDITIONALLY when the queried regime key isn't registered in its `_components` dict
  — which is exactly what happens whenever the real signal sits under any key OTHER than
  `"unknown"` (since `"unknown"` would then be null and never registered). The result:
  for `default_regime` in `{mean_reversion, chop, trending}`, the very first forecast is
  computed ONE BAR EARLY, from whatever partial history has accumulated (as little as 2
  bars), silently ignoring the configured `warmup` for that one bar.
  `default_regime="unknown"` is the one choice where this check is non-vacuous (the real
  block is registered under `"unknown"` itself), so it alone respects the configured
  warmup on every bar including the first. `mean_reversion`/`chop`/`trending` are
  otherwise mutually interchangeable (a pure, inert label choice among themselves) — but
  all three share this same one-bar defect that `"unknown"` alone avoids.
- **Known precedent, re-examined**: run_042 (H-041-C) shipped `default_regime:
  "mean_reversion"` with this exact empty-rules/components pattern. It carries the same
  mechanical defect (confirmed directly by instrumentation — it reports "ready" one bar
  before its own per-regime history reaches the configured warmup). It does not show up
  in run_042's own numbers for two independent, incidental reasons: its real `warmup=3`
  is so low the gap doesn't matter, AND `FearGreedContrarianComponent` only ever fires on
  UTC-midnight boundary bars, which the defect's fixed bar index doesn't happen to land
  on in that run. Neither is a safety property — do not read run_042 as proof that
  `mean_reversion` is an acceptable choice; the numeric near-miss was luck, not design.
  Use `"unknown"` for all new ungated configs.
- `validate_config.py` VIOLATION V10 enforces the concrete authoring mistake this pattern
  invites: if `regime_detector.components=[]` and `rules=[]`, `strategies.regimes
  [default_regime]` must not be null — that combination is silently dead (forecasts 0.0
  forever) with no error anywhere else to catch it.
- The underlying `main_strategy.is_ready()` one-bar defect itself is NOT fixed by this
  rule — it is a pre-existing, systemic effect on the very first ready bar of ANY
  strategy config (gated or ungated), invisible in aggregate metrics because it touches
  exactly one bar out of thousands. Using `default_regime="unknown"` sidesteps it for
  new ungated configs; it does not repair the engine. Flag for separate follow-up if you
  encounter it elsewhere — do not attempt to fix engine readiness semantics as a rider on
  an unrelated backtest_spec.

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
  reject it as VIOLATION V9. Use "unknown" only.
  (For a fully-ungated config — rules=[] AND components=[] — this restriction does not
  apply; see "Ungated hypotheses" above. Even there, use "unknown" as default_regime —
  it is the only choice that avoids a separate one-bar warmup-bypass defect, not because
  the other three are schema-forbidden.)
- Do not set default_regime to a regime that maps to null in the strategies block.
- Do not set any regime to {"components": []} (empty components list).
  If a regime should produce no trades, set it to null.
- Do not invent component class names. If you are unsure whether a variant is possible,
  read the component's row and the "Variant patterns" section of COMPONENT_CATALOG.md first. The answer is almost
  always "yes, achievable via a config parameter."

## Context rule
Read only the hypothesis artifacts, the design guide (STRATEGY_DESIGN_GUIDE.md) and the component catalogue
(COMPONENT_CATALOG.md). Minimal context.
