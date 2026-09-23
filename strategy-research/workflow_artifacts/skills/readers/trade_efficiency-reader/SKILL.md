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
Read this run's own `trade_efficiency.yaml` report (nothing else) and propose zero or more
concrete config changes (a `patch` against an existing component, or a `new_block` sketch)
targeting entry/exit/holding-sizing execution quality, each backed by evidence cited to a
specific field in this report. You propose; you do not decide the route.

## Required inputs
- `artifacts/reports/trade_efficiency.yaml` (Slice 5a,
  `strategy-research/tools/build_reports.py::build_trade_efficiency_report`.)
- `artifacts/grid_evaluation.yaml` (E-046b/Slice 2, already merged -- **optional**, see
  profitability-reader/SKILL.md's identical note; proceed without it if absent.)

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no `trade_diagnostics.json` directly, no
`campaign_state.yaml`, no `fragment_patterns.yaml`.

## Report shape (`trade_efficiency.yaml`)
```yaml
category: trade_efficiency
slices:
  overall:      # {source, ...verbatim trade_diagnostics_summary fields} OR unavailable
  per_window:   # {window_label: [trade_dict, ...]}  -- grouped from trade_diagnostics.json's
                # own `trades` list by each trade's `window` field, OR unavailable when
                # trade_diagnostics.json is absent/empty (only the overall pre-aggregate
                # summary exists in that case).
  per_symbol:   # {symbol: [trade_dict, ...]} -- same trades, grouped by `symbol`
  per_regime:   # {regime_label: [trade_dict, ...]} -- same trades, grouped by `regime_at_entry`
```
`slices.overall` carries whatever `trade_diagnostics_summary` held in `protocol_result.yaml`
-- per verdict-interpreter's own citations this typically includes `exit_efficiency_median`,
`entry_efficiency_median`, `pnl_concentration.pct_pnl_from_worst_decile_trades`,
`exit_reason_breakdown.{signal_flip_pct,stop_loss_pct}`, `stop_loss_recovery_rate`, and
`fee_reduction_metrics.{combine_nearby_trades,exit_later,enter_earlier,trade_less_often}`
sub-objects -- exact field set is per-run. `slices.per_window`/`per_symbol`/`per_regime` are
raw individual trade records (not pre-aggregated) when `trade_diagnostics.json` exists.

## Required outputs
- `artifacts/proposals/trade_efficiency.yaml`: a YAML list of 0+ proposal objects conforming
  to `workflow_artifacts/schemas/proposal.schema.json`. `[]` is a valid, honest output.

## Output requirements
Same proposal shape as every other reader (see `workflow_artifacts/schemas/proposal.schema.json`):
`proposal_id: trade_efficiency-<run_id>-<n>`, `kind: patch | new_block`, `patch`/`block`,
`evidence`, `scores.{confidence_real,distance_to_profitable,mechanism_plausibility}`,
`model_id`, `rubric_version: "trade_efficiency-reader-v1"`.

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. A `new_block`'s `block.config_paths` must list at least one path.

### `evidence` format rule
```yaml
# GOOD
evidence:
  - "slices.overall.exit_efficiency_median=0.44 (aggregate) but
     slices.overall.pnl_concentration.pct_pnl_from_worst_decile_trades=123% -- worst-decile
     trades dominate total PnL despite a positive-looking aggregate (aggregate-median caveat)."

# BAD
evidence:
  - "Exits are bad."
```

## Rules (carried forward from verdict-interpreter/SKILL.md's STEP 03 Trade Attribution and
IMPROVEMENT 10 Fee-reduction autopsy, adapted to read from `slices.overall`/grouped
`slices.per_window`/`per_symbol`/`per_regime` trade lists instead of `trade_diagnostics.json`
directly)

**Trade attribution decision table (STEP 03) — apply first matching pattern to
`slices.overall`'s fields:**

| Pattern | `primary_weakness` |
|---|---|
| High `mfe`, low realized return AND `exit_efficiency_median` < 0.30 | `exit` |
| `entry_efficiency_median` < -0.10 | `entry` |
| `pnl_concentration.pct_pnl_from_worst_decile_trades` > 80% (magnitude) AND `exit_reason_breakdown.signal_flip_pct` > 70% | `holding_sizing` (no stop mechanism; applies even when `stop_loss_pct=0`) |
| `stop_loss_recovery_rate` > 0.50 AND `exit_reason_breakdown.stop_loss_pct` > 10% | `holding_sizing` (stops too tight) |
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
`slices.overall.fee_reduction_metrics` when present:**

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

| Score | `confidence_real` | `distance_to_profitable` | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `slices.overall` is unavailable, or `slices.per_window`/`per_symbol`/`per_regime` all unavailable (no `trade_diagnostics.json`) leaving only a pre-aggregated summary with no per-trade evidence to cite. | Trade-attribution pattern shows `none_healthy` -- no identified weakness to close a gap on. | The attribution pattern fires on a single window's trade group only, with no corroboration from `per_symbol`/`per_regime` grouping of the same trades. |
| 1 | `slices.overall` populated but `slices.per_window` groups mostly have < 5 trades each. | `primary_weakness` identified but `distance` unclear -- e.g. `entry_efficiency_median` just past -0.10, no magnitude context. | Pattern recurs in 2 trade groups (e.g. 2 windows) with no other field corroborating. |
| 2 | `slices.overall` populated, `slices.per_window`/`per_symbol` show the same `primary_weakness`-supporting pattern in 2+ groups. | `primary_weakness` clearly identified, magnitude moderate (e.g. `pct_pnl_from_worst_decile_trades` in the 80-110% range). | Pattern recurs across 3+ groups AND at least one `fee_reduction_metrics` sub-field corroborates the same direction. |
| 3 | Trade-attribution pattern holds consistently across `per_window`, `per_symbol`, AND `per_regime` groupings of the same underlying trades. | Metric is close to flipping the attribution table's threshold the other way (e.g. `stop_loss_recovery_rate` well above 0.50, clearly indicating stops-too-tight rather than a marginal call). | Fee-reduction candidate and trade-attribution `primary_weakness` point to the SAME execution mechanism (e.g. both indicate exit timing), giving a coherent causal story, not two unrelated coincidences. |

## Checklist
- Apply the trade-attribution table to `slices.overall` first; only escalate to per-group
  evidence (`per_window`/`per_symbol`/`per_regime`) for corroboration, never to override the
  aggregate pattern with a cherry-picked group.
- Check `pnl_concentration.pct_pnl_from_worst_decile_trades` before ever writing
  `none_healthy` on the strength of a positive `exit_efficiency_median` alone.
- Every `evidence` entry cites a `slices.*` field path from THIS report.

## Forbidden
- Do not read or cite any other category's `reports/*.yaml`, `verdict_interpretation.yaml`,
  or `fragment_patterns.yaml`.
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate` anywhere in `proposals/trade_efficiency.yaml`.
- Do not propose discarding the underlying signal component when `primary_weakness` is
  `entry`/`exit`/`holding_sizing` -- these are execution-level, not signal-quality, findings.
- Do not invent component classes, transform ops, or regime names absent from
  `STRATEGY_DESIGN_GUIDE.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/trade_efficiency.yaml` and, if present,
`artifacts/grid_evaluation.yaml`. Minimal context.
