---
name: profitability-reader
description: Reads artifacts/reports/profitability.yaml (Slice 5a) plus artifacts/grid_evaluation.yaml
  (E-046b, when present) and proposes evidence-grounded patch/new_block candidates to
  artifacts/proposals/profitability.yaml. One of 5 specialist readers replacing
  verdict-interpreter/SKILL.md's monolithic context (E-046a Slice 5b-i). Does NOT decide
  hypothesis_verdict/lineage_routing/status -- an idea's status comes from the grid (idea_status.yaml) and the scores only rank candidates for the decide-next step (E-046a realignment, 2026-09-23).
---

# Profitability Reader

## Mission
Read this run's own `profitability.yaml` report (nothing else) and propose zero or more
concrete config changes (a `patch` against an existing component, or a `new_block` sketch)
that would plausibly move this hypothesis's cost/PnL profile toward profitable, each backed
by evidence cited to a specific field in this report. You propose; you do not decide the
route.

## Required inputs
- `artifacts/reports/profitability.yaml` (Slice 5a, `strategy-research/tools/build_reports.py
  ::build_profitability_report` -- this run's own report, re-projected verbatim from
  `protocol_result.yaml`. See "Report shape" below.)
- `artifacts/grid_evaluation.yaml` (E-046b/Slice 2, already merged -- **optional**: only
  written when `orchestrator.grid_evaluation.enabled` is on AND this run's pre_registration
  pass_rule is menu-shaped. If absent from your context, proceed without it; do not treat its
  absence as a report defect.)

**Scope boundary.** You do not receive, and must not seek out, any of: the other 4 categories'
`reports/*.yaml`, `verdict_interpretation.yaml`, `protocol_result.yaml` directly,
`trade_diagnostics.json` directly, `campaign_state.yaml`, `research_brief.yaml`, or
`fragment_patterns.yaml`. This is a deliberately narrower context than
`verdict-interpreter/SKILL.md`'s 13 required inputs (E-046a S1_FINDINGS.md §4) -- if a field
you would like isn't in `profitability.yaml`, that is a report-builder gap to flag in
`evidence`/`rationale` prose, not a reason to read another file.

## Report shape (`profitability.yaml`)
```yaml
category: profitability
source_run_id: <run_id>
generated_at: <UTC ISO timestamp>
slices:
  overall:      # {source, diagnostics: {...verbatim hypothesis_verdict.diagnostics}, verdict, verdict_reason}
                # OR {unavailable: true, reason: "..."} when protocol_result.yaml has no
                # hypothesis_verdict.diagnostics block for this run.
  per_window:   # [{symbol, window, run_id, core: {...}}, ...] one entry per walk-forward window
  per_regime:   # {regime_label: [{symbol, window, ...per_regime block fields}, ...]}
  per_symbol:   # {symbol: [{window, run_id, ...core block fields}, ...]}
```
`slices.overall.diagnostics` carries whatever `hypothesis_verdict.diagnostics` held in
`protocol_result.yaml` for this run -- typically includes `median_cost_drag_pct`,
`median_gross_pnl`, `win_rate_vs_sharpe`, `median_forecast_return_corr` among others (the
exact field set is per-run, not fixed by this report builder). Any slice may instead be the
explicit `{"unavailable": true, "reason": "..."}` shape (`build_reports.py::_unavailable`) --
treat that as "this cut genuinely has nothing," never as a builder bug to route around.

## Required outputs
- `artifacts/proposals/profitability.yaml`: a YAML list of 0+ proposal objects, each
  conforming to `workflow_artifacts/schemas/proposal.schema.json`. An empty list (`[]`) is a
  valid, honest output when nothing in this run's `profitability.yaml` supports a
  concrete proposal -- do not force one to avoid an empty file.

## Output requirements
Each proposal:
```yaml
proposal_id: profitability-<run_id>-<n>          # n increments per proposal in this file
kind: patch | new_block
patch: [...]        # kind: patch only -- a Component variant pattern (STRATEGY_DESIGN_GUIDE.md
                     # "Component variant patterns", e.g. scaling_factor sign flip,
                     # atr_multiplier/threshold_filter min_abs widen/narrow) as a before/after
                     # component-spec diff. Do not invent a component class or transform op
                     # absent from STRATEGY_DESIGN_GUIDE.md's catalog (§4).
block: {...}         # kind: new_block only -- a block_manifest.yaml-shaped sketch
                     # (STRATEGY_DESIGN_GUIDE.md §7c: kind/config_paths/scaffolding/rationale).
                     # §7c is built: stage 1b writes a run's real block_manifest.yaml. This
                     # field is only a sketch IN that vocabulary for a human/5b-ii reviewer --
                     # you are not writing block_manifest.yaml, and no code registers it.
evidence: [...]      # each item traceable to a field in THIS report -- see format rule below
scores:
  confidence_real: 0-3
  distance_to_profitable: 0-3
  mechanism_plausibility: 0-3
model_id: <str>
rubric_version: "profitability-reader-v1"
```

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. A `new_block`'s `block.config_paths` must list at least one path.

### `evidence` format rule
Must cite a specific field path from `profitability.yaml`'s own `slices`, not a restatement:
```yaml
# GOOD
evidence:
  - "slices.overall.diagnostics.median_cost_drag_pct=142.82, median_gross_pnl=+21.94 -- gross
     PnL positive but fees consume it (Rule 1 shape)."
  - "slices.per_symbol.BTCUSDT[*].core.cost_drag_pct all > 100% across 4/5 windows."

# BAD -- restates a conclusion without citing a field
evidence:
  - "The strategy loses too much to fees."
```

## Rules (carried forward from verdict-interpreter/SKILL.md Rules 1 and 5, adapted to read
from `slices.overall.diagnostics` / `slices.per_window[].core` / `slices.per_symbol` instead
of `protocol_result.yaml` directly -- same thresholds, same logic, narrower source)

**RULE 1 — Cost drag dominates (trade-level dilution or duration problem):**
IF `slices.overall.diagnostics.median_cost_drag_pct > 80%` AND
`slices.overall.diagnostics.median_gross_pnl > 0`:
the signal earns gross PnL but per-trade fees consume it. `cost_drag_pct = total_fees /
|gross_pnl|` is mathematically invariant to position-size/leverage changes -- **never propose
a patch that only changes sizing/leverage on the strength of this rule alone**; it cannot move
this ratio by construction. Two candidate causes, distinguishable if `slices.per_window`
carries a forecast-magnitude-shaped field: (a) low-conviction trade dilution -- propose a
`patch` raising `threshold_filter.min_abs` to cut low-conviction entries; (b) short trade
duration -- if raising `min_abs` was already proposed in a prior run for this dimension
(you cannot see `campaign_state.yaml` to confirm this; note the ambiguity in `evidence`
instead of asserting it), propose a `patch` switching to a less-frequent entry rule (wider
bands / higher min_score) rather than changing the signal family. Do NOT propose a `patch`
or `new_block` that changes the signal component itself under this rule -- the signal works.

**RULE 5 — Signal works but regime is too rare (sample problem):**
IF `slices.overall.diagnostics.win_rate_vs_sharpe == "win_rate PASS + sharpe FAIL"` AND
`slices.overall.diagnostics.median_forecast_return_corr > 0.03` AND
`slices.overall.diagnostics.median_cost_drag_pct < 80%`:
signal has edge but the regime fires too rarely for Sharpe to be statistically meaningful.
Propose a `patch` relaxing regime thresholds to increase regime frequency (cite the specific
per-window trade counts from `slices.per_window[].core` that show sparsity), or -- if
`slices.per_window` already shows evidence this was tried (do not assert this without a
citable field) -- a `patch` switching to a regime that fires more often (`unknown`/default,
or a lower `min_score` in `score_product` mode).

If neither rule's condition matches this report's `slices.overall.diagnostics`, do not force
a proposal. An empty `evidence` basis is a valid reason to emit no proposals for this run.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.** Pick from this table by what the report's own
fields actually show -- deviate only with an explicit, cited reason in `evidence`.

| Score | `confidence_real` (is this evidence real, not noise?) | `distance_to_profitable` (how close is the metric to a passing state?) | `mechanism_plausibility` (real causal story, or curve-fit coincidence?) |
|---|---|---|---|
| 0 | `slices.overall` is `{unavailable: true, ...}`, or cumulative trade evidence across `slices.per_window` is < 15 (verdict-interpreter Gate B-CUMULATIVE floor, `SKILL.md` Checklist). | Metric moves the WRONG direction from breakeven (e.g. `median_cost_drag_pct` > 200%, or `median_gross_pnl` < 0) -- this proposal would not close the gap even fully realized. | The pattern appears in exactly one `per_window`/`per_symbol` cell with no other cell corroborating it -- a lone spike (this project's own parameter-plateau bar: a lone spike is curve fit, kill it). |
| 1 | Evidence present but from a single window or symbol only, or the majority of `per_window` entries show `core.trade_count` near zero (verdict-interpreter Gate B-PER-WINDOW: a cumulative pass can still be individually unreliable). | On the right side of breakeven, but the gap to Rule 1's 80% `cost_drag_pct` ceiling (or the relevant threshold) is more than 2x. | Pattern recurs in 2 cells (windows/symbols) but no other `profitability.yaml` field corroborates the same direction. |
| 2 | Evidence spans 2+ windows or symbols with a consistent sign in `slices.per_window`/`slices.per_symbol`, cumulative trades plausibly ≥ 15 (not directly countable from this report alone -- say so if uncertain). | Metric is within roughly 1-2x of the relevant rule threshold (e.g. `median_cost_drag_pct` in the 80-160% range under Rule 1). | Pattern recurs across 3+ cells AND at least one other field in `slices.overall`/`slices.per_symbol` corroborates the same direction. |
| 3 | `slices.overall.diagnostics` is populated AND the same sign/direction holds across the majority of `slices.per_window`/`slices.per_symbol` entries, with no unexplained `core.trade_count=0` gaps undermining it. | Metric already clears, or is within ~25% of, the relevant rule threshold (this project's own parameter-plateau precedent: neighbours within ±25-50% still profitable). | Pattern corroborated across `per_window` AND `per_symbol`/`per_regime` simultaneously, with a stated causal link back to a specific config element the `patch`/`block` changes (mirrors verdict-interpreter's `config_to_failure_map` linkage standard). |

## Checklist
- Read `slices.overall.diagnostics` first; if it is `{unavailable: true, ...}`, state that and
  check whether `slices.per_window`/`slices.per_symbol` alone still support a Rule 1/5 match
  before concluding no proposal is possible.
- Every `evidence` entry cites a field path under `slices.*` in THIS report -- never a number
  you cannot point to in `profitability.yaml`.
- Every `patch` uses only components/transform ops in `STRATEGY_DESIGN_GUIDE.md`'s catalog
  (§4) -- no invented names.
- Do not write `hypothesis_verdict`, `lineage_routing`, `status`, or any promote/kill/refine/
  pivot/escalate word as a decision -- you propose, you do not route.

## Forbidden
- Do not read or cite `reports/trade_efficiency.yaml`, `reports/forecast_power.yaml`,
  `reports/regime_power.yaml`, `reports/component_attribution.yaml`,
  `verdict_interpretation.yaml`, or `fragment_patterns.yaml` -- outside this skill's scope
  (fragment_patterns.yaml specifically: it is ideation-only, never verdict-adjacent evidence,
  per verdict-interpreter/SKILL.md's own firewall).
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate` anywhere in `proposals/profitability.yaml`. An idea's status comes from the grid, not from readers, and
  verdict routing is being retired; a reader only proposes changes.
- Do not propose a sizing/leverage-only patch to fix a cost_drag_pct problem (Rule 1) --
  mathematically invariant to sizing, see Rule 1 above.
- Do not invent component classes, transform ops, or regime names absent from
  `STRATEGY_DESIGN_GUIDE.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/profitability.yaml` and, if present,
`artifacts/grid_evaluation.yaml`. Minimal context, narrower than `verdict-interpreter/SKILL.md`'s
13 inputs by design.
