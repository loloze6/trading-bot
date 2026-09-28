---
name: regime_power-reader
description: Reads artifacts/reports/regime_power.yaml (Slice 5a) plus artifacts/grid_evaluation.yaml
  (E-046b, when present) and proposes evidence-grounded patch/new_block candidates to
  artifacts/proposals/regime_power.yaml. One of 5 specialist readers replacing
  verdict-interpreter/SKILL.md's monolithic context (E-046a Slice 5b-i). Does NOT decide
  hypothesis_verdict/lineage_routing/status -- an idea's status comes from the grid (idea_status.yaml) and the scores only rank candidates for the decide-next step (E-046a realignment, 2026-09-23).
---

# Regime Power Reader

## Mission
Read this run's own `regime_power.yaml` report (nothing else) and propose zero or more
concrete config changes (a `patch` against an existing component/regime config, or a
`new_block` sketch) addressing regime-gate quality (detector confidence, hindsight-lag,
regime-informativeness), each backed by evidence cited to a specific field in this report.
You propose; you do not decide the route.

## Required inputs
- `artifacts/reports/regime_power.yaml` (Slice 5a,
  `strategy-research/tools/build_reports.py::build_regime_power_report`.)
- `artifacts/grid_evaluation.yaml` (E-046b/Slice 2, already merged -- **optional**, see
  profitability-reader/SKILL.md's identical note; proceed without it if absent.)

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no `regime_audit_decision.yaml`, no
`regime_detector_report.yaml` directly (a summarized, re-projected form of it is already
inside `variants.base.slices.overall.detector_health` -- read it there), no
`fragment_patterns.yaml`.

## Report shape (`regime_power.yaml`)

**E-061 C2 S2d ("experts see every variant," D-003): every graded variant of this idea gets its
own `slices` under `variants.<vid>` -- no separate base-only top-level `slices` (G8). `kind`/
`symbol` are `null` until E-061 C2 S2b lands.**

```yaml
category: regime_power
source_run_id: <run_id>
generated_at: <UTC ISO timestamp>
schema_version: 2
variants:
  base:
    kind: base | null
    symbol: <SYMBOL> | null
    status: graded          # "backtested and graded," never a pass/fail verdict (that's the grid's job)
    slices:
      overall:
        detector_health:  # re-projection of strategy-research/regime_detector_report.yaml
                           # (CAMPAIGN-LEVEL, not necessarily generated from THIS variant's exact
                           # config -- config_source field says which config it was measured
                           # against; treat a mismatch as a reason to lower confidence_real, not
                           # to discard the field), OR unavailable if that file doesn't exist.
        note:              # fixed text: E-040's regime-power checks name 3 items (a) label vs
                           # ignoring it, (b) hindsight-lag, (c) detector health; this report
                           # computes only (b) and (c) -- (a) is never claimed here.
      per_window:   # [{symbol, window, run_id, per_regime, regime_validity, hindsight_lag}, ...]
                    # hindsight_lag: {live_transition_count, hindsight_transition_count, lags_bars,
                    #   median_lag_bars, reason} OR unavailable when bars.csv is missing for that window.
      per_regime:   # {regime_label: [{symbol, window, per_regime, regime_validity}, ...]}
      per_symbol:   # {symbol: [same shape as per_window entries]}
  design_1: {kind: design | null, symbol: ..., status: graded, slices: {...same shape...}}
  asset_1:  {kind: asset  | null, symbol: ..., status: graded, slices: {...same shape...}}
failed_variants:      # {<vid>: reason} -- E-061 C2 S2a (D-015). Never a `variants` entry.
untested_variants:    # {<vid>: reason} -- card D. Also never a `variants` entry.
```
A variant's row may also carry `coverage: "partial, windows run N of M"` (E-061 C2 S2b/S2d, D-042) when it graded on fewer windows than the run protocol -- absent entirely when its coverage is full.
`hindsight_lag` is [NEW COMPUTATION] per `build_reports.py`'s own docstring -- a lag-only
measure (bar-distance between a live regime transition and the nearest hindsight-optimal-
direction transition), never a correctness claim. A positive `median_lag_bars` is expected
for a causal detector; it says nothing about whether the live label was the *right* one.

**Every rule and score below reads `variants.base.slices...`** -- `base` is the variant whose
config a `patch` proposal actually changes (decide_next resolves patches against the source
base config, one coin per variant, D-016). A `design`/`asset` variant's own `slices` are read
only for the cross-variant check immediately below, never as a substitute base for a rule.

**Cross-variant check (E-061 C2 S2d, D-016, one coin per variant):** before scoring, compare
`variants.base.slices` against every `variants.design_*.slices` and `variants.asset_*.slices`
present. A result that holds on `base` AND every `design` variant but NOT on an `asset` variant
is coin-specific evidence, not a general regime-gate property -- cite both variants in
`evidence` and lower `confidence_real` accordingly rather than generalizing. Note that
`detector_health` is campaign-level (not per-variant, per-coin) -- this check applies to
`hindsight_lag`/`per_regime`/`regime_validity`, not to `detector_health` itself.

## Retune-firewall awareness (not wired yet — this is 5b-ii's orchestration job, not this
skill's)
`_validate_retune_firewall` (`run_phase1_research.py:3481-3494`) rejects any
`regime_audit_decision.yaml.recommended_action` string containing `pnl`, `sharpe`, `ic`,
`backtest`, `cost_drag`, `forecast_return_corr`, `per_trade`, or `expectancy`. This reader is
not currently called from behind that guard -- 5b-ii's orchestrator-loop scope
(S1_FINDINGS.md §3/§8) is what will eventually move the guard-and-inject pair to run before
this reader specifically. Nothing here implements that wiring. But because this reader's own
scoped inputs never include cost/PnL-shaped fields in the first place (they live in
`profitability.yaml`/`trade_efficiency.yaml`, which you do not read), a
`regime_power.yaml`-grounded proposal naturally cannot cite them either -- phrase any
regime-detector-retune `patch`/`block` rationale around `detector_health`/`hindsight_lag`
fields only, never around a pnl/sharpe/cost_drag number you would have had to import from
another category's report to know. If you ever find yourself wanting to cite a cost or PnL
figure to justify a regime-detector change, that is itself a sign that proposal belongs in a
different reader's evidence, not this one's.

## Required outputs
- `artifacts/proposals/regime_power.yaml`: a YAML list of 0+ proposal objects conforming to
  `workflow_artifacts/schemas/proposal.schema.json`. `[]` is a valid, honest output.

## Output requirements
Same proposal shape as every other reader: `proposal_id: regime_power-<run_id>-<n>`,
`kind: patch | new_block`, `patch`/`block`, `evidence`,
`scores.{confidence_real,distance_to_profitable,mechanism_plausibility}`, `model_id`,
`rubric_version: "regime_power-reader-v1"`.

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. A `new_block`'s `block.config_paths` must list at least one path.

### `requires_feed` (optional -- only when this report shows the need)
Either `kind` may carry ONE extra field saying the proposal needs a data feed:
```yaml
requires_feed:
  feed: open_interest   # lowercase snake_case, from your handoff's feed_names (below)
  reason: "<why the result turns on that data, naming the regime_power.yaml field it rests on>"
```
Emit it only when a field of THIS report shows the missing data would plausibly change the
result, and cite that field in both `reason` and `evidence`. Never invent a need: a proposal
that can be tested on the data the run already used carries no `requires_feed`, and "more
data might help" is not evidence. It is not a third `kind` -- the proposal still carries its
`patch` or `block` sketch.

**Feed names -- one vocabulary.** Your handoff's `injected_context.feed_names` lists the
canonical names: `wired` (the engine's FEED_REGISTRY, usable today), `reserved` (built, but
declined until a data-policy designation covers them) and `wishlist_only` (named in
`campaign_record/feed_wishlist.yaml`, never built). When one of them names the data you mean,
use it exactly -- never a synonym (`oi` or `open_interest_data` for a listed `open_interest`).
Coin a new lowercase snake_case name (e.g. `open_interest`, `order_book_depth`,
`liquidations`) only when none fits.

What happens next is not yours to decide: for a feed that is not wired the pipeline files one
request per feed in `campaign_record/data_requests.yaml` (an acquisition, or a designation for
a reserved feed), and decide-next keeps the proposal waiting (infeasible) while that feed is
not wired and the config it would test reads it. It never changes this idea's status or route.
`tools/reader_proposals.py` rejects any other shape (a missing or empty `reason`, a
non-snake_case `feed`, an extra key), which stops the pipeline.

### `evidence` format rule
```yaml
# GOOD
evidence:
  - "variants.base.slices.per_window[2].hindsight_lag.median_lag_bars=14 (window run_2024w03); 3/5 windows
     show median_lag_bars > 10, suggesting the detector confirms transitions late relative to
     hindsight-optimal direction."

# BAD
evidence:
  - "The regime detector is slow."
```

## Rules (carried forward from verdict-interpreter/SKILL.md Rule 4 and IMPROVEMENT 02's
Regime Attribution Gate, adapted to read from `variants.base.slices.overall.detector_health` /
`variants.base.slices.per_window`/`per_regime` instead of `regime_detector_report.yaml`/
`protocol_result.yaml` directly)

**RULE 4 — Regime is uninformative:**
IF a regime appears across `variants.base.slices.per_regime` with consistently near-zero
`regime_validity.forward_return_mean`: FIRST check `regime_validity.n_bars` for that regime.
Compute (or estimate from the entries you can see) the median `n_bars` across the windows in
`variants.base.slices.per_regime[<regime>]`. IF median `n_bars` < 20: the near-zero
`forward_return_mean` is likely noise from an insufficient sample -- do NOT propose a
regime-redefinition `new_block` on this evidence; propose (or defer to) a threshold-relaxation
`patch` instead, since the regime fires too rarely to judge, not that it's uninformative. IF
median `n_bars` >= 20: propose a `new_block` for a different regime definition (e.g.
`score_product` mode instead of `threshold_rules`, or different component thresholds) --
cite the exact `n_bars` and `forward_return_mean` values driving the call.

**IMPROVEMENT 02 — Regime Attribution Gate (evidence-shaping, not a verdict):** this reader
does not receive `ungated_escape_eligible` or `regime_detector_confidence` (those live in the
handoff/regime-auditor artifacts, outside this reader's scoped inputs) -- so you cannot
independently reproduce verdict-interpreter's full 2-branch decision tree here. For reference
only (you do NOT decide among these -- see Forbidden below), verdict-interpreter/SKILL.md's
own `regime_attribution.conclusion` enum has exactly four values: `signal_bad_everywhere`,
`signal_good_wrong_regime_gate`, `signal_good_regime_gate_correct`, and
`inconclusive_low_detector_confidence`. What you CAN do from `variants.base.slices.overall.detector_health`:
if `detector_health.per_symbol_per_timeframe` (or whatever confidence-shaped field the
campaign-level report carries for this run's symbol/timeframe) reads low/medium rather than
high, note that explicitly in `evidence` and lower `confidence_real` on any regime-conditional
proposal accordingly -- do not assert any of the four `conclusion` values above yourself; they
are verdict-interpreter's/5b-ii's routing vocabulary, not this reader's to decide.

If neither Rule 4's condition nor a detector-health signal is present in this report, do not
force a proposal.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.**

| Score | `confidence_real` | `distance_to_profitable` | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `variants.base.slices.overall.detector_health` is unavailable, or the regime cell's median `n_bars` < 20 (Rule 4's own sample floor). | `detector_health`/`hindsight_lag` shows no informative signal at all (e.g. zero live transitions per `hindsight_lag.reason`, a "constant single-label window"). | The uninformative-regime or lag pattern appears in exactly one `per_window`/`per_regime` cell. |
| 1 | Evidence from `variants.base.slices.overall` only, `detector_health.config_source` does not clearly match this run's own config (mismatch noted per the report-shape note above). | `median_lag_bars` or `forward_return_mean` marginally off from a healthy reading, no clear magnitude framing. | Pattern recurs in 2 `per_window` entries, no `per_regime`/`per_symbol` corroboration. |
| 2 | `variants.base.slices.per_window`/`per_regime` show the median `n_bars` >= 20 AND the same near-zero-return or lag pattern in 2+ windows. | `median_lag_bars` clearly elevated (well above the detector's typical bar-count-to-transition ratio implied by `live_transition_count`/`hindsight_transition_count`) or `forward_return_mean` clearly near zero with a reliable sample. | Pattern recurs across 3+ `per_window`/`per_regime` cells AND `detector_health` (if present) is consistent with the same conclusion (e.g. low confidence + high lag together). |
| 3 | `variants.base.slices.overall.detector_health` populated with a matching `config_source` AND the pattern holds across the majority of `per_window` AND `per_regime` entries with `n_bars` >= 20 throughout. | Both `hindsight_lag.median_lag_bars` and the relevant `regime_validity` fields point unambiguously to the same fix direction (e.g. consistently high lag AND a reliable near-zero `forward_return_mean`). | Corroborated across `per_window`, `per_regime`, AND `detector_health` simultaneously, with a stated causal story tying the regime definition (not the underlying signal) to the observed pattern. |

## Checklist
- Always check `regime_validity.n_bars` before treating any `forward_return_mean` reading as
  conclusive (Rule 4's sample floor).
- Never phrase a `patch`/`block` rationale in cost/pnl/sharpe terms -- see the
  retune-firewall-awareness section above.
- Every `evidence` entry cites a `variants.base.slices.*` field path from THIS report.

## Forbidden
- Do not read or cite `reports/profitability.yaml`, `reports/trade_efficiency.yaml`,
  `reports/forecast_power.yaml`, `reports/component_attribution.yaml`,
  `verdict_interpretation.yaml`, `regime_audit_decision.yaml`, or `fragment_patterns.yaml`.
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate`/`signal_bad_everywhere`-style routing vocabulary anywhere in
  `proposals/regime_power.yaml`.
- Do not phrase a regime-detector-retune proposal's `evidence`/`rationale` using any of the
  retune-firewall's forbidden terms (`pnl`, `sharpe`, `ic`, `backtest`, `cost_drag`,
  `forecast_return_corr`, `per_trade`, `expectancy`) -- even though the firewall isn't wired
  to this reader yet, writing content that would violate it once wired is exactly what this
  note exists to prevent.
- Do not invent component classes, transform ops, or regime names absent from
  `STRATEGY_DESIGN_GUIDE.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/regime_power.yaml` and, if present,
`artifacts/grid_evaluation.yaml`. Minimal context.
