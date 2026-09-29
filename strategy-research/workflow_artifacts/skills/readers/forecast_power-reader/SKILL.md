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
- `artifacts/registry_summary.yaml` (E-061 C2 S2e -- written by code before the readers run from the campaign's block registry and this run's manifest; read it **only** for `distance_to_profitable`, see "Distance to profitable" below. It is the one extra input allowed beyond this category's report and the grid.)

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no `protocol_result.yaml` directly, no
`campaign_state.yaml`, no `fragment_patterns.yaml`. The registry itself (`block_registry.yaml`) stays out of scope: `registry_summary.yaml` is its only reader-facing view.

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
    status: graded          # "backtested and graded," never a pass/fail verdict (that's the grid's job)
    slices:
      overall:      # {median_forecast_return_corr, median_forecast_return_corr_source,
                    #  prescreen_backtest_cross_check} -- any subset present, or unavailable when
                    # neither hypothesis_verdict.diagnostics.median_forecast_return_corr nor
                    # prescreen_backtest_cross_check exist for this variant.
      per_window:   # [{symbol, window, run_id, forecast_return_corr, forecast_return_corr_pvalue}, ...]
      per_regime:   # {regime_label: [{symbol, window, ...regime_validity block fields incl. n_bars,
                    #  forward_return_mean}, ...]}
      per_symbol:   # {symbol: [{window, forecast_return_corr, forecast_return_corr_pvalue}, ...]}
  design_1: {kind: design | null, symbol: ..., status: graded, slices: {...same shape...}}
  asset_1:  {kind: asset  | null, symbol: ..., status: graded, slices: {...same shape...}}
failed_variants:      # {<vid>: reason} -- E-061 C2 S2a (D-015). Never a `variants` entry.
untested_variants:    # {<vid>: reason} -- card D. Also never a `variants` entry.
```
A variant's row may also carry `coverage: "partial, windows run N of M"` (E-061 C2 S2b/S2d, D-042) when it graded on fewer windows than the run protocol -- absent entirely when its coverage is full.

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
`rubric_version: "forecast_power-reader-v2"`.

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

| Score | `confidence_real` | `distance_to_profitable` (card I / D-017: how far is this block from what the registry already holds? -- NOT closeness to a rule threshold; see "Distance to profitable" below) | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `variants.base.slices.overall` is unavailable, or the corr's own regime cell has `n_bars` median < 20 per the regime-validity context above. | A `patch` (never a `new_block` sketch) on an idea that is itself a registered block (`registry_summary.yaml` `this_run.patches_registered_block` is set), or a `patch` on this run when `this_run.idea_status` is `validated` (this run's own block is registered only after the readers, so the summary cannot list it yet), or the same block type as a registered one (`this_run.type_already_registered` is true / a `relation_to_this_run` of `same_type` or `same_classes_timeframe_unknown` row -- the latter is an assumed match: a timeframe category is unrecorded on one side). | Corr crosses the ±0.03 threshold in exactly one `per_window` entry, opposite sign or near-zero in the rest -- a lone spike. |
| 1 | Evidence from `variants.base.slices.overall` only, no `per_window`/`per_symbol` corroboration in the same direction. | Same component classes as a registered block but a different timeframe category or kind (`relation_to_this_run` is `same_classes_different_timeframe_category`, `same_classes_different_kind` or `same_classes_different_kind_and_timeframe_category`), OR this run's measured `|correlation to the composite|` is >= 0.6 (`this_run.correlation_to_composite.max_abs`). | Pattern (Rule 2 no-edge or Rule 3 inversion) recurs in 2 `per_window` entries, no `per_regime`/`per_symbol` corroboration. |
| 2 | `variants.base.slices.per_window` shows the same sign/magnitude-range in the majority of windows. | The block type is not in the registry, and `max_abs` is 0.3-0.6 or cannot be measured (`status` `not_measurable` or `skipped: ...`, or `no_residual_ic_artifact` while `registry.n_forecast_blocks` > 0 -- correlation was never computed, so it is not measurable, or `this_run.block_type` is null) -- every `new_block` sketch lands here unless row 0 or 1 applies. | Pattern recurs across 3+ `per_window` entries AND `variants.base.slices.per_regime`/`per_symbol` shows the same direction for at least one grouping. |
| 3 | `variants.base.slices.overall.median_forecast_return_corr` populated AND the same sign holds across the majority of `per_window` AND `per_symbol` entries, with no thin-regime (`n_bars` < 20) cell driving the reading. | The block type is not in the registry AND (`max_abs` < 0.3, or no composite exists yet: `status` `no_composite`, or `no_residual_ic_artifact` with `registry.n_forecast_blocks` = 0) -- it fills a missing block type with low correlation to the registry. | Corroborated across `per_window`, `per_symbol`, AND `per_regime` simultaneously, with a stated causal story (e.g. "inversion consistent with betting against a mean-reverting signal read as momentum"). |

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
`artifacts/grid_evaluation.yaml`, plus `artifacts/registry_summary.yaml` (the one extra input; used only for `distance_to_profitable`). Minimal context.
