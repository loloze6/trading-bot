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

**E-061 C2 S2d ("experts see every variant," D-003): every graded variant of this idea (`base`,
zero or more `design`, zero or more `asset`) gets its own `slices` block under `variants.<vid>`
-- there is no separate base-only top-level `slices` (saves tokens: G8). `kind`/`symbol` are
`null` until E-061 C2 S2b lands (it adds them to `artifacts/variants/index.yaml`); never assume
a value when they're null.**

```yaml
category: profitability
source_run_id: <run_id>
generated_at: <UTC ISO timestamp>
schema_version: 2
variants:
  base:                          # always present when any variant of this idea graded this run
    kind: base | null            # null until E-061 C2 S2b
    symbol: <SYMBOL> | null      # null until E-061 C2 S2b
    status: graded          # "backtested and graded," never a pass/fail verdict (that's the grid's job)
    slices:
      overall:      # {source, diagnostics: {...verbatim hypothesis_verdict.diagnostics}, verdict, verdict_reason}
                    # OR {unavailable: true, reason: "..."} when THIS VARIANT's protocol_result.yaml
                    # has no hypothesis_verdict.diagnostics block for this run.
      per_window:   # [{symbol, window, run_id, core: {...}}, ...] one entry per walk-forward window
      per_regime:   # {regime_label: [{symbol, window, ...per_regime block fields}, ...]}
      per_symbol:   # {symbol: [{window, run_id, ...core block fields}, ...]}
  design_1: {kind: design | null, symbol: ..., status: graded, slices: {...same shape...}}
  asset_1:  {kind: asset  | null, symbol: ..., status: graded, slices: {...same shape...}}
failed_variants:      # {<vid>: reason} -- E-061 C2 S2a (D-015): a variant of this idea that was
                      # validated going into the backtest but produced no graded result this run
                      # (a crash, or refused before any backtest touched data). NEVER a `variants`
                      # entry -- do not look for its `slices` there.
untested_variants:    # {<vid>: reason} -- another variant of this idea with no graded result in
                      # THIS run (skipped as an exact repeat, declined by the data gate, refused
                      # by config validation). Also never a `variants` entry.
```
A variant's row may also carry `coverage: "partial, windows run N of M"` (E-061 C2 S2b/S2d, D-042) when it graded on fewer windows than the run protocol -- absent entirely when its coverage is full.
`variants.<vid>.slices.overall.diagnostics` carries whatever `hypothesis_verdict.diagnostics`
held in that variant's own `protocol_result.yaml` -- typically includes `median_cost_drag_pct`,
`median_gross_pnl`, `win_rate_vs_sharpe`, `median_forecast_return_corr` among others (the
exact field set is per-run, not fixed by this report builder). Any slice may instead be the
explicit `{"unavailable": true, "reason": "..."}` shape (`build_reports.py::_unavailable`) --
treat that as "this cut genuinely has nothing," never as a builder bug to route around.

**Every rule and score below reads `variants.base.slices...`** -- `base` is the variant whose
config a `patch` proposal actually changes (decide_next resolves patches against the source
base config, one coin per variant, D-016). A `design`/`asset` variant's own `slices` are read
only for the cross-variant check immediately below, never as a substitute base for a rule.

**Cross-variant check (E-061 C2 S2d, D-016, one coin per variant):** before scoring, compare
`variants.base.slices` against every `variants.design_*.slices` and `variants.asset_*.slices`
present. A result that holds on `base` AND every `design` variant but NOT on an `asset` variant
is **coin-specific evidence, not a general property of the signal** -- cite both the base/design
variant(s) and the asset variant explicitly in `evidence`, and lower `confidence_real`
accordingly rather than generalizing a base-only (or base+design-only) pattern to "the
strategy." A `failed_variants`/`untested_variants` entry (this idea is then at best
inconclusive, D-014/card D) does not itself change a graded variant's own evidence -- it only
means fewer variants are available for this cross-check; note the gap in `evidence` if it
matters to your proposal.

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
requires_feed: {feed, reason}   # optional -- see below
```

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. A `new_block`'s `block.config_paths` must list at least one path.

### `requires_feed` (optional -- only when this report shows the need)
Either `kind` may carry ONE extra field saying the proposal needs a data feed:
```yaml
requires_feed:
  feed: open_interest   # lowercase snake_case, from your handoff's feed_names (below)
  reason: "<why the result turns on that data, naming the profitability.yaml field it rests on>"
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
Must cite a specific field path from `profitability.yaml`'s own `slices`, not a restatement:
```yaml
# GOOD
evidence:
  - "variants.base.slices.overall.diagnostics.median_cost_drag_pct=142.82, median_gross_pnl=+21.94 -- gross
     PnL positive but fees consume it (Rule 1 shape)."
  - "variants.base.slices.per_symbol.BTCUSDT[*].core.cost_drag_pct all > 100% across 4/5 windows."

# BAD -- restates a conclusion without citing a field
evidence:
  - "The strategy loses too much to fees."
```

## Rules (carried forward from verdict-interpreter/SKILL.md Rules 1 and 5, adapted to read
from `variants.base.slices.overall.diagnostics` / `variants.base.slices.per_window[].core` / `variants.base.slices.per_symbol` instead
of `protocol_result.yaml` directly -- same thresholds, same logic, narrower source)

**RULE 1 — Cost drag dominates (trade-level dilution or duration problem):**
IF `variants.base.slices.overall.diagnostics.median_cost_drag_pct > 80%` AND
`variants.base.slices.overall.diagnostics.median_gross_pnl > 0`:
the signal earns gross PnL but per-trade fees consume it. `cost_drag_pct = total_fees /
|gross_pnl|` is mathematically invariant to position-size/leverage changes -- **never propose
a patch that only changes sizing/leverage on the strength of this rule alone**; it cannot move
this ratio by construction. Two candidate causes, distinguishable if `variants.base.slices.per_window`
carries a forecast-magnitude-shaped field: (a) low-conviction trade dilution -- propose a
`patch` raising `threshold_filter.min_abs` to cut low-conviction entries; (b) short trade
duration -- if raising `min_abs` was already proposed in a prior run for this dimension
(you cannot see `campaign_state.yaml` to confirm this; note the ambiguity in `evidence`
instead of asserting it), propose a `patch` switching to a less-frequent entry rule (wider
bands / higher min_score) rather than changing the signal family. Do NOT propose a `patch`
or `new_block` that changes the signal component itself under this rule -- the signal works.

**RULE 5 — Signal works but regime is too rare (sample problem):**
IF `variants.base.slices.overall.diagnostics.win_rate_vs_sharpe == "win_rate PASS + sharpe FAIL"` AND
`variants.base.slices.overall.diagnostics.median_forecast_return_corr > 0.03` AND
`variants.base.slices.overall.diagnostics.median_cost_drag_pct < 80%`:
signal has edge but the regime fires too rarely for Sharpe to be statistically meaningful.
Propose a `patch` relaxing regime thresholds to increase regime frequency (cite the specific
per-window trade counts from `variants.base.slices.per_window[].core` that show sparsity), or -- if
`variants.base.slices.per_window` already shows evidence this was tried (do not assert this without a
citable field) -- a `patch` switching to a regime that fires more often (`unknown`/default,
or a lower `min_score` in `score_product` mode).

If neither rule's condition matches this report's `variants.base.slices.overall.diagnostics`, do not force
a proposal. An empty `evidence` basis is a valid reason to emit no proposals for this run.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.** Pick from this table by what the report's own
fields actually show -- deviate only with an explicit, cited reason in `evidence`.

| Score | `confidence_real` (is this evidence real, not noise?) | `distance_to_profitable` (how close is the metric to a passing state?) | `mechanism_plausibility` (real causal story, or curve-fit coincidence?) |
|---|---|---|---|
| 0 | `variants.base.slices.overall` is `{unavailable: true, ...}`, or cumulative trade evidence across `variants.base.slices.per_window` is < 15 (verdict-interpreter Gate B-CUMULATIVE floor, `SKILL.md` Checklist). | Metric moves the WRONG direction from breakeven (e.g. `median_cost_drag_pct` > 200%, or `median_gross_pnl` < 0) -- this proposal would not close the gap even fully realized. | The pattern appears in exactly one `per_window`/`per_symbol` cell with no other cell corroborating it -- a lone spike (this project's own parameter-plateau bar: a lone spike is curve fit, kill it). |
| 1 | Evidence present but from a single window or symbol only, or the majority of `per_window` entries show `core.trade_count` near zero (verdict-interpreter Gate B-PER-WINDOW: a cumulative pass can still be individually unreliable). | On the right side of breakeven, but the gap to Rule 1's 80% `cost_drag_pct` ceiling (or the relevant threshold) is more than 2x. | Pattern recurs in 2 cells (windows/symbols) but no other `profitability.yaml` field corroborates the same direction. |
| 2 | Evidence spans 2+ windows or symbols with a consistent sign in `variants.base.slices.per_window`/`variants.base.slices.per_symbol`, cumulative trades plausibly ≥ 15 (not directly countable from this report alone -- say so if uncertain). | Metric is within roughly 1-2x of the relevant rule threshold (e.g. `median_cost_drag_pct` in the 80-160% range under Rule 1). | Pattern recurs across 3+ cells AND at least one other field in `variants.base.slices.overall`/`variants.base.slices.per_symbol` corroborates the same direction. |
| 3 | `variants.base.slices.overall.diagnostics` is populated AND the same sign/direction holds across the majority of `variants.base.slices.per_window`/`variants.base.slices.per_symbol` entries, with no unexplained `core.trade_count=0` gaps undermining it. | Metric already clears, or is within ~25% of, the relevant rule threshold (this project's own parameter-plateau precedent: neighbours within ±25-50% still profitable). | Pattern corroborated across `per_window` AND `per_symbol`/`per_regime` simultaneously, with a stated causal link back to a specific config element the `patch`/`block` changes (mirrors verdict-interpreter's `config_to_failure_map` linkage standard). |

## Checklist
- Read `variants.base.slices.overall.diagnostics` first; if it is `{unavailable: true, ...}`, state that and
  check whether `variants.base.slices.per_window`/`variants.base.slices.per_symbol` alone still support a Rule 1/5 match
  before concluding no proposal is possible.
- Every `evidence` entry cites a field path under `variants.base.slices.*` in THIS report -- never a number
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
