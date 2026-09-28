---
name: forecast_power-reader
description: Reads artifacts/reports/forecast_power.yaml (Slice 5a) plus artifacts/grid_evaluation.yaml
  (E-046b, when present) and proposes evidence-grounded patch/new_block candidates to
  artifacts/proposals/forecast_power.yaml. One of 5 specialist readers replacing
  verdict-interpreter/SKILL.md's monolithic context (E-046a Slice 5b-i). Does NOT decide
  hypothesis_verdict/lineage_routing/status -- an idea's status comes from the grid (idea_status.yaml) and the scores only rank candidates for the decide-next step (E-046a realignment, 2026-09-23).
---

# Forecast Power Reader

## Mission
Read this run's own `forecast_power.yaml` report (nothing else) and propose zero or more
concrete config changes (a `patch` against an existing component, or a `new_block` sketch)
addressing directional-edge quality (no edge / inverted edge / no diagnostic signal at all),
each backed by evidence cited to a specific field in this report. You propose; you do not
decide the route.

## Required inputs
- `artifacts/reports/forecast_power.yaml` (Slice 5a,
  `strategy-research/tools/build_reports.py::build_forecast_power_report`.)
- `artifacts/grid_evaluation.yaml` (E-046b/Slice 2, already merged -- **optional**, see
  profitability-reader/SKILL.md's identical note; proceed without it if absent.)

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no `protocol_result.yaml` directly, no
`campaign_state.yaml`, no `fragment_patterns.yaml`.

## Report shape (`forecast_power.yaml`)

**E-061 C2 S2d ("experts see every variant," D-003): every graded variant of this idea gets its
own `slices` under `variants.<vid>` -- no separate base-only top-level `slices` (G8). `kind`/
`symbol` are `null` until E-061 C2 S2b lands.**

```yaml
category: forecast_power
source_run_id: <run_id>
generated_at: <UTC ISO timestamp>
schema_version: 2
variants:
  base:
    kind: base | null
    symbol: <SYMBOL> | null
    status: validated
    slices:
      overall:      # {median_forecast_return_corr, median_forecast_return_corr_source,
                    #  prescreen_backtest_cross_check} -- any subset present, or unavailable when
                    # neither hypothesis_verdict.diagnostics.median_forecast_return_corr nor
                    # prescreen_backtest_cross_check exist for this variant.
      per_window:   # [{symbol, window, run_id, forecast_return_corr, forecast_return_corr_pvalue}, ...]
      per_regime:   # {regime_label: [{symbol, window, ...regime_validity block fields incl. n_bars,
                    #  forward_return_mean}, ...]}
      per_symbol:   # {symbol: [{window, forecast_return_corr, forecast_return_corr_pvalue}, ...]}
  design_1: {kind: design | null, symbol: ..., status: validated, slices: {...same shape...}}
  asset_1:  {kind: asset  | null, symbol: ..., status: validated, slices: {...same shape...}}
failed_variants:      # {<vid>: reason} -- E-061 C2 S2a (D-015). Never a `variants` entry.
untested_variants:    # {<vid>: reason} -- card D. Also never a `variants` entry.
```

**Every rule and score below reads `variants.base.slices...`** -- `base` is the variant whose
config a `patch` proposal actually changes (decide_next resolves patches against the source
base config, one coin per variant, D-016). A `design`/`asset` variant's own `slices` are read
only for the cross-variant check immediately below, never as a substitute base for a rule.

**Cross-variant check (E-061 C2 S2d, D-016, one coin per variant):** before scoring, compare
`variants.base.slices` against every `variants.design_*.slices` and `variants.asset_*.slices`
present. A result that holds on `base` AND every `design` variant but NOT on an `asset` variant
is coin-specific evidence, not a general directional-edge property -- cite both variants in
`evidence` and lower `confidence_real` accordingly rather than generalizing.

## Required outputs
- `artifacts/proposals/forecast_power.yaml`: a YAML list of 0+ proposal objects conforming to
  `workflow_artifacts/schemas/proposal.schema.json`. `[]` is a valid, honest output.

## Output requirements
Same proposal shape as every other reader: `proposal_id: forecast_power-<run_id>-<n>`,
`kind: patch | new_block`, `patch`/`block`, `evidence`,
`scores.{confidence_real,distance_to_profitable,mechanism_plausibility}`, `model_id`,
`rubric_version: "forecast_power-reader-v1"`.

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. A `new_block`'s `block.config_paths` must list at least one path.

### `requires_feed` (optional -- only when this report shows the need)
Either `kind` may carry ONE extra field saying the proposal needs a data feed:
```yaml
requires_feed:
  feed: open_interest   # lowercase snake_case, from your handoff's feed_names (below)
  reason: "<why the result turns on that data, naming the forecast_power.yaml field it rests on>"
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
  - "variants.base.slices.overall.median_forecast_return_corr=0.012 -- below the 0.03 no-edge floor
     (Rule 2); variants.base.slices.per_window shows corr < 0.03 in 4/5 windows."

# BAD
evidence:
  - "The signal doesn't predict returns well."
```

## Rules (carried forward from verdict-interpreter/SKILL.md Rules 2, 3, and 6, adapted to
read from `variants.base.slices.overall`/`variants.base.slices.per_window`/`variants.base.slices.per_regime` instead of
`protocol_result.yaml` directly -- same thresholds, same logic, narrower source)

**RULE 2 — Signal has no directional edge:**
IF `abs(variants.base.slices.overall.median_forecast_return_corr) < 0.03` OR its p-value > 0.10 (check
`variants.base.slices.per_window[].forecast_return_corr_pvalue` if `overall` doesn't carry a pooled
p-value): the signal does not predict price direction. Propose a `new_block` for a
structurally different signal component -- changing this component's *parameters* under this
rule is not a fix (a `patch` would not address a no-edge finding); if you cannot propose a
concrete alternative component from `STRATEGY_DESIGN_GUIDE.md`'s catalog, state that in
`evidence` and emit no proposal rather than a vague `new_block`.

**RULE 3 — Signal is inverted:**
IF `variants.base.slices.overall.median_forecast_return_corr < -0.03` AND its p-value < 0.10: the signal
predicts the opposite of what the strategy bets. Propose a `patch` reversing the signal's
direction (e.g. `scaling_factor` sign flip -- see `STRATEGY_DESIGN_GUIDE.md`'s "Component
variant patterns" for the exact per-component sign-flip vocabulary, such as
`KeltnerBreakoutComponent`'s `scaling_factor: -20.0` for lower-band short instead of upper-band
long). This is a cheap `patch`, same component, reversed logic -- not a `new_block`.

**RULE 6 — No diagnostic signal (all metrics null):**
IF `variants.base.slices.overall.median_forecast_return_corr` is null/absent AND no other numeric field is
present in `variants.base.slices.overall`: distinguish using `variants.base.slices.per_symbol`/`variants.base.slices.per_window` trade
evidence if present in this report (this report does not carry `min_trade_count` directly --
if you cannot see per-symbol trade counts anywhere in `forecast_power.yaml`, say so and keep
`confidence_real` at 0 rather than guessing between the CASE A/CASE B split
verdict-interpreter's own Rule 6 makes; that split needs `per_symbol_summary.min_trade_count`,
which is a `profitability.yaml`/trade-count field outside this reader's scope). Do not
escalate timeframe or pivot the signal on Rule 6 alone from this report -- flag the
ambiguity as low-confidence evidence instead of forcing a proposal.

**Regime validity context** (from `variants.base.slices.per_regime`, used to corroborate Rule 2/3, not as
its own rule -- Rule 4's full regime-uninformative logic belongs to regime_power-reader, which
owns `per_regime`/`regime_validity` interpretation depth this reader does not): if
`variants.base.slices.per_regime[<regime>][].n_bars` is small (median < 20 across entries for a regime),
treat any near-zero `forward_return_mean` in that regime as noise, not as edge evidence one
way or the other -- do not let a thin regime cell inflate or deflate `confidence_real`.

If none of Rules 2/3/6 match this report's `variants.base.slices.overall`, do not force a proposal.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.**

| Score | `confidence_real` | `distance_to_profitable` | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `variants.base.slices.overall` is unavailable, or the corr's own regime cell has `n_bars` median < 20 per the regime-validity context above. | `median_forecast_return_corr` sign is wrong for the strategy's bet direction with p < 0.10 (clear inversion, Rule 3 territory but proposing the WRONG direction fix) -- or Rule 6's total-null case with no corroborating field anywhere. | Corr crosses the ±0.03 threshold in exactly one `per_window` entry, opposite sign or near-zero in the rest -- a lone spike. |
| 1 | Evidence from `variants.base.slices.overall` only, no `per_window`/`per_symbol` corroboration in the same direction. | `abs(corr)` between 0.03 and the nearest A8.6 `plausible_ic_upper` anchor floor for this signal's class (dense-OHLCV signals top out at 0.03-0.05 per this project's own empirical ceiling -- a corr just above 0.03 is barely past the no-edge floor, not close to a real ceiling). | Pattern (Rule 2 no-edge or Rule 3 inversion) recurs in 2 `per_window` entries, no `per_regime`/`per_symbol` corroboration. |
| 2 | `variants.base.slices.per_window` shows the same sign/magnitude-range in the majority of windows. | `abs(corr)` comfortably inside the signal class's `plausible_ic_upper` anchor range (hypothesis-design/SKILL.md A8.6 table) with the correct sign. | Pattern recurs across 3+ `per_window` entries AND `variants.base.slices.per_regime`/`per_symbol` shows the same direction for at least one grouping. |
| 3 | `variants.base.slices.overall.median_forecast_return_corr` populated AND the same sign holds across the majority of `per_window` AND `per_symbol` entries, with no thin-regime (`n_bars` < 20) cell driving the reading. | Corr already near or above the signal class's own A8.6 anchor ceiling with correct sign -- Rule 3's reversal, if proposed, would put it there. | Corroborated across `per_window`, `per_symbol`, AND `per_regime` simultaneously, with a stated causal story (e.g. "inversion consistent with betting against a mean-reverting signal read as momentum"). |

## Checklist
- Check `variants.base.slices.per_regime`'s `n_bars` before trusting any `forward_return_mean`-adjacent
  reading as edge evidence (regime-validity context above).
- Rule 2/6 → propose `new_block` (structurally different signal), never a parameter `patch`.
- Rule 3 → propose a `patch` (sign flip / reversed logic), never a `new_block`.
- Every `evidence` entry cites a `variants.base.slices.*` field path from THIS report.

## Forbidden
- Do not read or cite any other category's `reports/*.yaml`, `verdict_interpretation.yaml`,
  or `fragment_patterns.yaml`.
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate` anywhere in `proposals/forecast_power.yaml`.
- Do not attempt regime_power-reader's own `per_regime`/Rule-4-depth interpretation (e.g. a
  full regime-uninformative verdict) -- you may cite `variants.base.slices.per_regime` only as
  corroboration for a Rule 2/3/6 finding, never as your own primary rule.
- Do not invent component classes, transform ops, or regime names absent from
  `STRATEGY_DESIGN_GUIDE.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/forecast_power.yaml` and, if present,
`artifacts/grid_evaluation.yaml`. Minimal context.
