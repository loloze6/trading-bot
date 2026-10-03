---
name: trade_efficiency-reader
description: Reads artifacts/reports/trade_efficiency.yaml (Slice 5a) plus artifacts/grid_evaluation.yaml
  (E-046b, when present) and proposes evidence-grounded patch/new_block candidates to
  artifacts/proposals/trade_efficiency.yaml. One of 5 specialist readers replacing
  verdict-interpreter/SKILL.md's monolithic context (E-046a Slice 5b-i). Does NOT decide
  hypothesis_verdict/lineage_routing/status -- an idea's status comes from the grid (idea_status.yaml) and the scores only rank candidates for the decide-next step (E-046a realignment, 2026-09-23).
---

# Trade Efficiency Reader

## Mission
Read this run's own `trade_efficiency.yaml` report (with the inputs listed below) and propose zero or more
concrete config changes (a `patch` against an existing component, or a `new_block` sketch)
targeting entry/exit/holding-sizing execution quality, each backed by evidence cited to a
specific field in this report. You propose; you do not decide the route.

## Required inputs
- `artifacts/reports/trade_efficiency.yaml` (Slice 5a,
  `strategy-research/tools/build_reports.py::build_trade_efficiency_report`.)
- `artifacts/grid_evaluation.yaml` (E-046b/Slice 2, already merged -- **optional**, see
  profitability-reader/SKILL.md's identical note; proceed without it if absent.)
- **What was tested and what exists** (so you never invent a component or a setting -- run_065/run_066 readers did, because they had never seen the config):
  - `artifacts/hypothesis_card.yaml` -- the idea this run tested: its claim, signal and assumptions. Read your report as evidence about THIS claim.
  - `artifacts/block_manifest.yaml` (**optional**, absent on a composition run) -- which config paths are the tested block and which are scaffolding.
  - this run's base config (`artifacts/variants/<base>/strategy_config.json`, or `artifacts/candidate_strategy_config.json` without the variant loop) -- the real component ids and settings. A `patch`'s `component_id` is a component's `id` in this file, its `field` a path that exists inside that component, and `before` its current value; any other patch is refused when decide-next resolves it (`patch_unresolvable`).
  - `docs/COMPONENT_CATALOG.md` and `docs/STRATEGY_DESIGN_GUIDE.md` -- the same two documents step 2 gets: every component's settings and outputs, and what a config can and cannot express. A change the config cannot express (e.g. a stop-loss, or acting on a bar before it closes) is not a `patch`.
- `artifacts/registry_summary.yaml` (E-061 C2 S2e -- written by code before the readers run from the campaign's block registry and this run's manifest; read it **only** for `distance_to_profitable`, see "Distance to profitable" below.)

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no `trade_diagnostics.json` directly, no
`campaign_state.yaml`, no `fragment_patterns.yaml`. The registry itself (`block_registry.yaml`) stays out of scope: `registry_summary.yaml` is its only reader-facing view.

## Report shape (`trade_efficiency.yaml`)

**E-061 C2 S2d ("experts see every variant," D-003): every graded variant of this idea gets its
own `slices` under `variants.<vid>` -- no separate base-only top-level `slices` (G8). `kind`/
`symbol` are `null` until E-061 C2 S2b lands.**

```yaml
category: trade_efficiency
source_run_id: <run_id>
generated_at: <UTC ISO timestamp>
schema_version: 2
variants:
  base:
    kind: base | null
    symbol: <SYMBOL> | null
    status: graded          # "backtested and graded," never a pass/fail verdict (that's the grid's job)
    slices:
      overall:      # {source, ...verbatim trade_diagnostics_summary fields} OR unavailable
      per_window:   # {window_label: {n, <numeric field>: {mean, median, p10, p90}, ...}} --
                    # G7 COMPACTED AGGREGATE (E-061 C2 S2d) over that variant's own
                    # trade_diagnostics.json `trades` list grouped by each trade's `window`
                    # field, OR unavailable when that variant's trade_diagnostics.json is
                    # absent/empty (only the overall pre-aggregate summary exists then).
      per_symbol:   # {symbol: {n, <numeric field>: {...}}} -- same trades, grouped by `symbol`
      per_regime:   # {regime_label: {n, <numeric field>: {...}}} -- same trades, grouped by
                    # `regime_at_entry`
  design_1: {kind: design | null, symbol: ..., status: graded, slices: {...same shape...}}
  asset_1:  {kind: asset  | null, symbol: ..., status: graded, slices: {...same shape...}}
failed_variants:      # {<vid>: reason} -- E-061 C2 S2a (D-015). Never a `variants` entry.
untested_variants:    # {<vid>: reason} -- card D. Also never a `variants` entry.
```
A variant's row may also carry `coverage: "partial, windows run N of M"` (E-061 C2 S2b/S2d, D-042) when it graded on fewer windows than the run protocol -- absent entirely when its coverage is full.
`variants.<vid>.slices.overall` carries whatever `trade_diagnostics_summary` held in that
variant's own `protocol_result.yaml` -- per verdict-interpreter's own citations this typically
includes `exit_efficiency_median`, `entry_efficiency_median`,
`pnl_concentration.pct_pnl_from_worst_decile_trades`,
`exit_reason_breakdown.{signal_flip_pct,stop_loss_pct}`, `stop_loss_recovery_rate`, and
`fee_reduction_metrics.{combine_nearby_trades,exit_later,enter_earlier,trade_less_often}`
sub-objects -- exact field set is per-run. `variants.<vid>.slices.per_window`/`per_symbol`/
`per_regime` are **n/mean/median/p10/p90 aggregates over that variant's individual trade
records (G7 compaction), not the raw records themselves** -- `n` is the real trade count for
that group; a field's `mean`/`median`/`p10`/`p90` are real order statistics over the group's
trades, never a fabricated figure.

**Every rule and score below reads `variants.base.slices...`** -- `base` is the variant whose
config a `patch` proposal actually changes (decide_next resolves patches against the source
base config, one coin per variant, D-016). A `design`/`asset` variant's own `slices` are read
only for the cross-variant check immediately below, never as a substitute base for a rule.

**Cross-variant check (E-061 C2 S2d, D-016, one coin per variant):** before scoring, compare
`variants.base.slices` against every `variants.design_*.slices` and `variants.asset_*.slices`
present. A result that holds on `base` AND every `design` variant but NOT on an `asset` variant
is coin-specific evidence, not a general execution-quality property -- cite both variants in
`evidence` and lower `confidence_real` accordingly rather than generalizing.

## Required outputs
- `artifacts/proposals/trade_efficiency.yaml`: a YAML list of 0+ proposal objects conforming
  to `workflow_artifacts/schemas/proposal.schema.json`. `[]` is a valid, honest output.

## Output requirements
Same proposal shape as every other reader (see `workflow_artifacts/schemas/proposal.schema.json`):
`proposal_id: trade_efficiency-<run_id>-<n>`, `kind: patch | new_block`, `patch`/`block`,
`evidence`, `scores.{confidence_real,distance_to_profitable,mechanism_plausibility}`,
`model_id`, `rubric_version: "trade_efficiency-reader-v2"`.

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. **New-block shape (required, CUL-380):** a `new_block`'s `block` is exactly `{kind: forecast|regime, config_paths: [at least one JSON-pointer string], scaffolding: [optional], rationale: "<what the new block is and why it should help>"}`. `rationale` is the idea itself: if decide-next picks this proposal, it becomes the next run's research goal. A proposal missing any of this is dropped (the run continues, the drop is recorded).

### `requires_feed` (optional -- only when this report shows the need)
Either `kind` may carry ONE extra field saying the proposal needs a data feed:
```yaml
requires_feed:
  feed: open_interest   # lowercase snake_case, from your handoff's feed_names (below)
  reason: "<why the result turns on that data, naming the trade_efficiency.yaml field it rests on>"
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
  - "variants.base.slices.overall.exit_efficiency_median=0.44 (aggregate) but
     variants.base.slices.overall.pnl_concentration.pct_pnl_from_worst_decile_trades=123% -- worst-decile
     trades dominate total PnL despite a positive-looking aggregate (aggregate-median caveat)."

# BAD
evidence:
  - "Exits are bad."
```

## Rules (carried forward from verdict-interpreter/SKILL.md's STEP 03 Trade Attribution and
IMPROVEMENT 10 Fee-reduction autopsy, adapted to read from `variants.base.slices.overall`/grouped
`variants.base.slices.per_window`/`per_symbol`/`per_regime` trade lists instead of `trade_diagnostics.json`
directly)

**Trade attribution decision table (STEP 03) — apply first matching pattern to
`variants.base.slices.overall`'s fields:**

| Pattern | `primary_weakness` |
|---|---|
| High `mfe`, low realized return AND `exit_efficiency_median` < 0.30 | `exit` |
| `entry_efficiency_median` < -0.10 | `entry` |
| `pnl_concentration.pct_pnl_from_worst_decile_trades` > 80% (magnitude) AND `exit_reason_breakdown.signal_flip_pct` > 70% | `holding_sizing` (losing trades are held until the signal flips). The engine has no stop-loss setting a `patch` could add (STRATEGY_DESIGN_GUIDE.md: exits are not configurable) -- name the finding in `evidence`, and propose only a change the base config can express (e.g. a transform on the forecast), or nothing. |
| `stop_loss_recovery_rate` > 0.50 AND `exit_reason_breakdown.stop_loss_pct` > 10% | `holding_sizing` (stops too tight -- report it; a stop is not a config setting, so this is never a `patch`) |
| Poor `entry_efficiency_median`, poor `exit_efficiency_median` | `signal_direction` -- **do not propose a patch under this pattern alone**; forecast_power-reader owns signal-direction evidence, and you do not have `forecast_return_corr` in this report to confirm it. Note the pattern in `evidence` but keep `confidence_real` low unless another field here corroborates it. |
| None of the above | `none_healthy` -- do not force a proposal. |

**Aggregate-median caveat** (unchanged from verdict-interpreter): `exit_efficiency_median` is
pulled positive by winners even when losers have deeply negative exit efficiency. Check
`pnl_concentration.pct_pnl_from_worst_decile_trades` before concluding `none_healthy` solely
because `exit_efficiency_median` looks positive.

**Routing implication carried forward as a PROPOSAL-KIND rule, not a verdict:** when
`primary_weakness` is `entry`, `exit`, or `holding_sizing`, propose a `patch` at the
execution/parameter level (e.g. tighten/loosen a stop, adjust an exit rule's threshold) --
never a `new_block` that discards the underlying signal component. That is an
execution-level fix, not a signal-quality one.

**Fee-reduction autopsy (IMPROVEMENT 10) — pick `candidate_system` from
`variants.base.slices.overall.fee_reduction_metrics` when present:**

| Metric stands out | `candidate_system` |
|---|---|
| `combine_nearby_trades.same_direction_reentry_rate` high, `avg_reentry_gap_bars` small | `combine_nearby_trades` |
| `exit_later.avg_post_exit_drift_pct` meaningfully positive, `pct_better_exit_1bar_later` high | `exit_later` |
| `enter_earlier.avg_pre_entry_drift_pct` meaningfully positive, `pct_better_entry_1bar_earlier` high | `enter_earlier` |
| `trade_less_often.boundary_recross_rate` high or `frequency_vs_volatility_ratio` high | `trade_less_often` |

If `fee_reduction_metrics` is null or absent, propose from the trade-attribution table above
alone and note the gap in `evidence`. If more than one candidate stands out, pick the largest
deviation from "no problem" and say so.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.**

| Score | `confidence_real` | `distance_to_profitable` (card I / D-017: how far is this block from what the registry already holds? -- NOT closeness to a rule threshold; see "Distance to profitable" below) | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `variants.base.slices.overall` is unavailable, or `variants.base.slices.per_window`/`per_symbol`/`per_regime` all unavailable (no `trade_diagnostics.json`) leaving only a pre-aggregated summary with no per-trade evidence to cite. | A `patch` (never a `new_block` sketch) on an idea that is itself a registered block (`registry_summary.yaml` `this_run.patches_registered_block` is set), or a `patch` on this run when `this_run.idea_status` is `validated` (this run's own block is registered only after the readers, so the summary cannot list it yet), or the same block type as a registered one (`this_run.type_already_registered` is true / a `relation_to_this_run` of `same_type` or `same_classes_timeframe_unknown` row -- the latter is an assumed match: a timeframe category is unrecorded on one side). | The attribution pattern fires on a single window's trade group only, with no corroboration from `per_symbol`/`per_regime` grouping of the same trades. |
| 1 | `variants.base.slices.overall` populated but `variants.base.slices.per_window` groups mostly have < 5 trades each. | Same component classes as a registered block but a different timeframe category or kind (`relation_to_this_run` is `same_classes_different_timeframe_category`, `same_classes_different_kind` or `same_classes_different_kind_and_timeframe_category`), OR this run's measured `|correlation to the composite|` is >= 0.6 (`this_run.correlation_to_composite.max_abs`). | Pattern recurs in 2 trade groups (e.g. 2 windows) with no other field corroborating. |
| 2 | `variants.base.slices.overall` populated, `variants.base.slices.per_window`/`per_symbol` show the same `primary_weakness`-supporting pattern in 2+ groups. | The block type is not in the registry, and `max_abs` is 0.3-0.6 or cannot be measured (`status` `not_measurable` or `skipped: ...`, or `no_residual_ic_artifact` while `registry.n_forecast_blocks` > 0 -- correlation was never computed, so it is not measurable, or `this_run.block_type` is null) -- every `new_block` sketch lands here unless row 0 or 1 applies. | Pattern recurs across 3+ groups AND at least one `fee_reduction_metrics` sub-field corroborates the same direction. |
| 3 | Trade-attribution pattern holds consistently across `per_window`, `per_symbol`, AND `per_regime` groupings of the same underlying trades. | The block type is not in the registry AND (`max_abs` < 0.3, or no composite exists yet: `status` `no_composite`, or `no_residual_ic_artifact` with `registry.n_forecast_blocks` = 0) -- it fills a missing block type with low correlation to the registry. | Fee-reduction candidate and trade-attribution `primary_weakness` point to the SAME execution mechanism (e.g. both indicate exit timing), giving a coherent causal story, not two unrelated coincidences. |

### Distance to profitable (card I, D-017)

`distance_to_profitable` no longer measures closeness to a rule threshold. It scores how far the
proposed block is from what the registry already validated: 3 = fills a missing block type with low
correlation to the registry; 0 = a neighbour of something already validated. Read
`artifacts/registry_summary.yaml` (written by code before the readers run; the one input outside
this category's report and the grid you may read for this score):

- A block *type* is `(kind, sorted component classes, timeframe category)`. For a `patch`, the type
  is `this_run.block_type` (plus any component class the patch adds); for a `new_block` sketch use
  the sketch's `kind` and any component classes it names.
- `this_run.type_already_registered`, `this_run.neighbour_block_ids`,
  `this_run.patches_registered_block` and each `blocks[*].relation_to_this_run` (or, past 50 blocks,
  `groups[*]`) say whether the type is present and which registered blocks neighbour it.
  `relation_to_this_run` is one of `same_type` (kind, classes and timeframe category all verified equal),
  `same_classes_timeframe_unknown` (same kind and classes, but a timeframe category is unrecorded on one
  side: an ASSUMED same type, counted by `type_already_registered` -- say "assumed" in `evidence`),
  `same_classes_different_timeframe_category`, `same_classes_different_kind`,
  `same_classes_different_kind_and_timeframe_category`, or null (a different set of component classes;
  two empty sets count as the same set). Past 50 blocks `this_run.neighbour_block_ids` is capped;
  `this_run.n_neighbour_blocks` is the full count.
- `this_run.patches_registered_block` and the `this_run.idea_status` clause of row 0 apply to a `patch`
  proposal only, never to a `new_block` sketch (a sketch is scored on its own type).
- `this_run.correlation_to_composite`: use `max_abs` (the largest absolute correlation over the
  variants -- the conservative reading) when `status` is `measured`. `no_composite` means a residual-IC
  run found no composite to correlate against. `no_residual_ic_artifact` means the correlation was never
  computed, NOT that no composite exists: it is row 3 only when `registry.n_forecast_blocks` is 0 (nothing
  to build a composite from), otherwise "not measurable" (row 2). `not_measurable` and `skipped: ...` are
  "not measurable".
- If `this_run.block_type` is null (see `this_run.reason`) the type cannot be placed: score 2, unless a
  lower row applies (see the precedence rule below).
- Precedence (a lower score always wins -- conservative): check row 0 first (a `patch` whose
  `this_run.patches_registered_block` is set, a `patch` with `this_run.idea_status` `validated`, or a
  same-type / assumed-same-type block), then row 1 (a same-classes neighbour, or `max_abs` >= 0.6), then the
  null-type default of 2, then rows 2 and 3. So a null `block_type` scores 2 only when no row-0 or row-1
  condition holds, and never scores 3. The 0.3 / 0.6 cut-offs are rank-only placeholders:
  they order candidates for decide-next and never touch an idea's status or the holdout.
- Cite the `registry_summary.yaml` field that decided the score as one `evidence` item; every other
  `evidence` item still cites this category's own report. `confidence_real` and
  `mechanism_plausibility` anchors are unchanged.

## Checklist
- Apply the trade-attribution table to `variants.base.slices.overall` first; only escalate to per-group
  evidence (`per_window`/`per_symbol`/`per_regime`) for corroboration, never to override the
  aggregate pattern with a cherry-picked group.
- Check `pnl_concentration.pct_pnl_from_worst_decile_trades` before ever writing
  `none_healthy` on the strength of a positive `exit_efficiency_median` alone.
- Every `evidence` entry cites a `variants.base.slices.*` field path from THIS report.

## Forbidden
- Do not read or cite any other category's `reports/*.yaml`, `verdict_interpretation.yaml`,
  or `fragment_patterns.yaml`.
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate` anywhere in `proposals/trade_efficiency.yaml`.
- Do not propose discarding the underlying signal component when `primary_weakness` is
  `entry`/`exit`/`holding_sizing` -- these are execution-level, not signal-quality, findings.
- Do not invent component classes, transform ops, or regime names absent from
  `COMPONENT_CATALOG.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/trade_efficiency.yaml` and, if present,
`artifacts/grid_evaluation.yaml`, plus `artifacts/registry_summary.yaml` (the one extra input; used only for `distance_to_profitable`). Minimal context.
