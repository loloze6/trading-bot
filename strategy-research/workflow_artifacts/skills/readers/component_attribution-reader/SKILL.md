---
name: component_attribution-reader
description: Reads artifacts/reports/component_attribution.yaml (Slice 5a) plus
  artifacts/grid_evaluation.yaml (E-046b, when present) and proposes evidence-grounded
  patch/new_block candidates to artifacts/proposals/component_attribution.yaml. One of 5
  specialist readers replacing verdict-interpreter/SKILL.md's monolithic context (E-046a
  Slice 5b-i). Unlike the other 4 readers, this category has NO existing rule-block analog in
  verdict-interpreter/SKILL.md -- its rules below are new content, authored for this build
  (see "Rules" section's own reasoning). Does NOT decide hypothesis_verdict/lineage_routing/
  status -- an idea's status comes from the grid (idea_status.yaml) and the scores only rank candidates for the decide-next step (E-046a realignment, 2026-09-23).
---

# Component Attribution Reader

## Mission
Read this run's own `component_attribution.yaml` report (with the inputs listed below) and propose zero or
more concrete config changes (a `patch` against an existing component, or a `new_block`
sketch) grounded in per-bar component-level evidence -- which individual strategy component
is behaving in a way worth tuning, and why -- each backed by evidence cited to a specific
field in this report. You propose; you do not decide the route.

**Why this reader's rules are new content, not an adaptation:** `verdict-interpreter/SKILL.md`
has no rule block that reads individual component debug output (S1_FINDINGS.md §4: "component
attribution has no obvious existing rule-block analog"). The rules below were authored
directly from `build_reports.py::build_component_attribution_report`'s real output shape and
general "what would make a component's own attribution evidence-worthy" reasoning -- see each
rule's own justification.

## Required inputs
- `artifacts/reports/component_attribution.yaml` (Slice 5a,
  `strategy-research/tools/build_reports.py::build_component_attribution_report`.)
- `artifacts/grid_evaluation.yaml` (E-046b/Slice 2, already merged -- **optional**, see
  profitability-reader/SKILL.md's identical note; proceed without it if absent.)
- **What was tested and what exists** (so you never invent a component or a setting -- run_065/run_066 readers did, because they had never seen the config):
  - `artifacts/hypothesis_card.yaml` -- the idea this run tested: its claim, signal and assumptions. Read your report as evidence about THIS claim.
  - `artifacts/block_manifest.yaml` (**optional**, absent on a composition run) -- which config paths are the tested block and which are scaffolding.
  - this run's base config (`artifacts/variants/<base>/strategy_config.json`, or `artifacts/candidate_strategy_config.json` without the variant loop) -- the real component ids and settings. A `patch`'s `component_id` is a component's `id` in this file, its `field` a path that exists inside that component, and `before` its current value; any other patch is refused when decide-next resolves it (`patch_unresolvable`).
  - `docs/COMPONENT_CATALOG.md` and `docs/STRATEGY_DESIGN_GUIDE.md` -- the same two documents step 2 gets: every component's settings and outputs, and what a config can and cannot express. A change the config cannot express (e.g. a stop-loss, or acting on a bar before it closes) is not a `patch`.
- `artifacts/registry_summary.yaml` (E-061 C2 S2e -- written by code before the readers run from the campaign's block registry and this run's manifest; read it **only** for `distance_to_profitable`, see "Distance to profitable" below.)

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no raw `bars.csv` directly (this report
already extracted the `debug_info.components.*` columns for you), no `fragment_patterns.yaml`. The registry itself (`block_registry.yaml`) stays out of scope: `registry_summary.yaml` is its only reader-facing view.

## Report shape (`component_attribution.yaml`)

**E-061 C2 S2d ("experts see every variant," D-003; G7 compaction): every graded variant of
this idea gets its own `slices` under `variants.<vid>` -- no separate base-only top-level
`slices` (G8). `kind`/`symbol` are `null` until E-061 C2 S2b lands. G7 ALSO changed the shape
of `per_window`/`per_regime`/`per_symbol` themselves: they are now n/mean/median/p10/p90
AGGREGATES per (group, component), not raw per-bar records -- read the note on each field
below carefully, it reverses this reader's earlier "zero aggregation" framing.**

```yaml
category: component_attribution
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
        components_discovered: [<name>, ...]   # sorted list of component names found in ANY
                                                # window's bars.csv debug_info.components.* columns
                                                # -- inventory only, this list itself is never aggregated.
        note: "inventory only ... G7-compacted per-component aggregates below, not raw per-bar rows."
        # OR {unavailable: true, reason: "..."} when no debug_info.components.*.* columns exist
        # in any window's bars.csv for this variant.
      per_window:   # {window_label: {component: {n, <metric>: {mean, median, p10, p90}, ...}, ...}}
                    # n/mean/median/p10/p90 AGGREGATES (E-061 C2 S2d, G7) over every bar of
                    # that window for that component -- NOT one record per bar.
      per_regime:   # {regime_label: {component: {n, <metric>: {...}}, ...}} -- excludes the
                    # trailing blank-regime boundary row (build_reports.py's own CODE-REVIEW
                    # FIX, 2026-09-21), pooled across every window sharing that regime label.
      per_symbol:   # {symbol: {component: {n, <metric>: {...}}, ...}} -- pooled across every
                    # window sharing that symbol.
  design_1: {kind: design | null, symbol: ..., status: graded, slices: {...same shape...}}
  asset_1:  {kind: asset  | null, symbol: ..., status: graded, slices: {...same shape...}}
failed_variants:      # {<vid>: reason} -- E-061 C2 S2a (D-015). Never a `variants` entry.
untested_variants:    # {<vid>: reason} -- card D. Also never a `variants` entry.
```
A variant's row may also carry `coverage: "partial, windows run N of M"` (E-061 C2 S2b/S2d, D-042) when it graded on fewer windows than the run protocol -- absent entirely when its coverage is full.
Each aggregate's `n` is the real count of (bar, component) records pooled into that group; a
field's `mean`/`median`/`p10`/`p90` are real order statistics over that group's per-bar values
(whatever metric columns that component's `debug_info.components.<name>.*` emitted -- field
names are component-specific and not fixed ahead of time), never a fabricated figure. Any
statistic you cite must be one of these four values (or `n`) as given -- you cannot see
individual bar values anymore, so do not claim a pattern ("mostly zero," "spikes on entry")
that needs a finer grain than n/mean/median/p10/p90 to support.

**Every rule and score below reads `variants.base.slices...`** -- `base` is the variant whose
config a `patch` proposal actually changes (decide_next resolves patches against the source
base config, one coin per variant, D-016). A `design`/`asset` variant's own `slices` are read
only for the cross-variant check immediately below, never as a substitute base for a rule.

**Cross-variant check (E-061 C2 S2d, D-016, one coin per variant):** before scoring, compare
`variants.base.slices` against every `variants.design_*.slices` and `variants.asset_*.slices`
present. A component pattern that holds on `base` AND every `design` variant but NOT on an
`asset` variant is coin-specific evidence, not a general property of that component -- cite
both variants in `evidence` and lower `confidence_real` accordingly rather than generalizing.

## Required outputs
- `artifacts/proposals/component_attribution.yaml`: a YAML list of 0+ proposal objects
  conforming to `workflow_artifacts/schemas/proposal.schema.json`. `[]` is a valid, honest
  output -- this report is raw per-bar data with no pre-aggregation, so a run with many
  components but no distinguishable pattern should produce few or zero proposals rather than
  a forced one per component.

## Output requirements
Same proposal shape as every other reader: `proposal_id: component_attribution-<run_id>-<n>`,
`kind: patch | new_block`, `patch`/`block`, `evidence`,
`scores.{confidence_real,distance_to_profitable,mechanism_plausibility}`, `model_id`,
`rubric_version: "component_attribution-reader-v2"`. `kind: patch` is expected to dominate
here (tuning an existing component's `weight`/`scaling_factor`/threshold per
`COMPONENT_CATALOG.md`'s "Variant patterns"); `kind: new_block` applies only
when the evidence shows an existing component's regime-conditional behavior that NO current
component captures well (see Rule CA-2 below).

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. **New-block shape (required, CUL-380):** a `new_block`'s `block` is exactly `{kind: forecast|regime, config_paths: [at least one JSON-pointer string], scaffolding: [optional], rationale: "<what the new block is and why it should help>"}`. `rationale` is the idea itself: if decide-next picks this proposal, it becomes the next run's research goal. A proposal missing any of this is dropped (the run continues, the drop is recorded).

### `requires_feed` (optional -- only when this report shows the need)
Either `kind` may carry ONE extra field saying the proposal needs a data feed:
```yaml
requires_feed:
  feed: open_interest   # lowercase snake_case, from your handoff's feed_names (below)
  reason: "<why the result turns on that data, naming the component_attribution.yaml field it rests on>"
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
  - "variants.base.slices.overall.components_discovered=['rsi','keltner'];
     variants.base.slices.per_regime.trending.keltner={n: 42, weighted_contribution: {mean: 1.8,
     median: 1.6, p10: 0.4, p90: 3.9}}, while variants.base.slices.per_regime.mean_reversion.
     keltner={n: 38, weighted_contribution: {mean: 0.0, median: 0.0, p10: 0.0, p90: 0.0}} --
     keltner appears inert outside trending."

# BAD
evidence:
  - "The keltner component isn't contributing much."
```

## Rules (new territory -- authored for this reader; no existing analog in
verdict-interpreter/SKILL.md)

**RULE CA-1 — Degenerate/constant output is not evidence-worthy on its own:**
If a component's aggregate for a metric in `variants.base.slices.per_window[<window>]` has
`p10 == median == p90` (or all four of `mean`/`median`/`p10`/`p90` equal) across an ENTIRE
window's group, that component's output was constant across every bar pooled into it -- not
tunable via a parameter `patch` in that window. Do not propose a `patch` adjusting
`weight`/`scaling_factor` for a component that shows no variation to tune in the first place;
flag it in `evidence` as a wiring/config concern instead (e.g. "component X's
`weighted_contribution` aggregate for window Y is {n: 96, mean: 0.0, median: 0.0, p10: 0.0,
p90: 0.0} -- likely gated off or misconfigured, not a tuning target"), and keep
`confidence_real` low unless the same constant-output pattern recurs consistently enough to be
a genuine, reportable finding rather than a proposal.
*Justification:* a component with zero observed variation (p10 == p90) offers no basis to judge
which direction a `weight`/`scaling_factor` change would even push it -- proposing a tuning
patch on constant data is unfalsifiable by construction.

**RULE CA-2 — Regime-conditional divergence IS evidence-worthy:**
If a component's aggregates in `variants.base.slices.per_regime` show a materially different
range or central tendency across regime labels (e.g. `mean`/`median` clearly away from zero
with a wide `p10`-`p90` spread in one regime's group, near-constant/near-zero in another),
that divergence is evidence-worthy. Propose a `patch` adjusting that component's `weight` or a
regime-specific parameter if the config already supports per-regime component sets (per
`STRATEGY_DESIGN_GUIDE.md`'s "The forecast for each regime": components differ per regime already, per
`strategies.regimes.<regime>.components`) -- or a `new_block` sketch if the divergence suggests
a genuinely new, regime-specific component would capture the pattern better than tuning the
existing one.
*Justification:* this project's regime-gate architecture already assumes components can
differ by regime (`STRATEGY_DESIGN_GUIDE.md` "Ungated" and "Worked examples") -- a
component's own aggregate behaving differently across regimes is the most direct
component-level signal this report can offer that a regime-specific config change is worth
proposing, without needing any cross-category (profitability/pnl) evidence to justify it.

**RULE CA-3 — Cross-window inconsistency in `components_discovered` is informational, not a
tuning proposal:**
If a component name appears in some windows' `per_window`/`per_regime` aggregates but is
absent from others within the SAME run, note this explicitly in `evidence` as a possible
wiring/config inconsistency (e.g. a component conditionally emitted, or a config that changed
between windows) rather than silently proposing a tuning patch on top of possibly-inconsistent
data. Keep `confidence_real` at 0-1 for any proposal touching that component until the
inconsistency itself is understood.
*Justification:* attribution built on a component that isn't even consistently present across
this run's own windows cannot support a confident tuning claim -- the inconsistency itself is
more informative than any pattern built on top of it, and reporting it as a finding (even with
no proposal attached) is more honest than papering over it.

If none of CA-1/CA-2/CA-3 identify a genuine pattern in this report, do not force a proposal.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.**

| Score | `confidence_real` | `distance_to_profitable` (card I / D-017: how far is this block from what the registry already holds? -- NOT closeness to a rule threshold; see "Distance to profitable" below) | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `variants.base.slices.overall` is unavailable (no `debug_info.components.*` columns anywhere), or the pattern rests on a component with constant aggregate output (Rule CA-1) or cross-window inconsistency (Rule CA-3). | A `patch` (never a `new_block` sketch) on an idea that is itself a registered block (`registry_summary.yaml` `this_run.patches_registered_block` is set), or a `patch` on this run when `this_run.idea_status` is `validated` (this run's own block is registered only after the readers, so the summary cannot list it yet), or the same block type as a registered one (`this_run.type_already_registered` is true / a `relation_to_this_run` of `same_type` or `same_classes_timeframe_unknown` row -- the latter is an assumed match: a timeframe category is unrecorded on one side). | The divergence/degeneracy appears in exactly one window's aggregate with no corroboration elsewhere. |
| 1 | Evidence from a single window's `per_window` aggregate only, no `per_regime`/`per_symbol` corroboration of the same component. | Same component classes as a registered block but a different timeframe category or kind (`relation_to_this_run` is `same_classes_different_timeframe_category`, `same_classes_different_kind` or `same_classes_different_kind_and_timeframe_category`), OR this run's measured `|correlation to the composite|` is >= 0.6 (`this_run.correlation_to_composite.max_abs`). | Pattern recurs in 2 aggregate groups (windows or regimes) for the same component, no third corroborating grouping. |
| 2 | `variants.base.slices.per_regime` shows the same divergence pattern for a component across 2+ regime labels' aggregates, consistently. | The block type is not in the registry, and `max_abs` is 0.3-0.6 or cannot be measured (`status` `not_measurable` or `skipped: ...`, or `no_residual_ic_artifact` while `registry.n_forecast_blocks` > 0 -- correlation was never computed, so it is not measurable, or `this_run.block_type` is null) -- every `new_block` sketch lands here unless row 0 or 1 applies. | Pattern recurs across 3+ aggregate groups (windows/regimes/symbols) for the same component. |
| 3 | The same component's divergence pattern holds across `per_window`, `per_regime`, AND `per_symbol` aggregates simultaneously, with `components_discovered` confirming consistent presence across all windows (ruling out CA-3). | The block type is not in the registry AND (`max_abs` < 0.3, or no composite exists yet: `status` `no_composite`, or `no_residual_ic_artifact` with `registry.n_forecast_blocks` = 0) -- it fills a missing block type with low correlation to the registry. | Corroborated across `per_window`, `per_regime`, AND `per_symbol` for the same component, with a stated causal story (e.g. "component X's signal is regime-specific by design intent -- its near-zero aggregate outside trending is consistent, not broken -- so the proposal narrows its weight to the regime where it demonstrably varies"). |

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
- Confirm variation exists (`p10` != `p90`, Rule CA-1) before proposing any tuning `patch`.
- Confirm the component's presence is consistent across this run's windows (Rule CA-3) before
  building confidence on a cross-window pattern.
- Every `evidence` entry cites a `variants.base.slices.*` aggregate (component name + n/mean/
  median/p10/p90) from THIS report -- never a finer-grained per-bar value this report no
  longer carries, and never a statistic beyond those four you cannot point to directly.

## Forbidden
- Do not read or cite `reports/profitability.yaml`, `reports/trade_efficiency.yaml`,
  `reports/forecast_power.yaml`, `reports/regime_power.yaml`, `verdict_interpretation.yaml`,
  raw `bars.csv`, or `fragment_patterns.yaml`.
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate` anywhere in `proposals/component_attribution.yaml`.
- Do not propose a tuning `patch` for a component whose aggregate shows `p10 == p90` (constant
  across every bar cited, Rule CA-1) -- there is nothing to tune toward.
- Do not compute or assert a statistic (correlation, a percentile other than p10/p90, "mostly
  zero" beyond what `n`/`mean`/`median`/`p10`/`p90` show) you cannot show directly in the
  listed aggregates -- this report performs ONLY n/mean/median/p10/p90 aggregation (G7);
  neither should you invent a finer one silently.
- Do not invent component classes, transform ops, or regime names absent from
  `COMPONENT_CATALOG.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/component_attribution.yaml` and, if present,
`artifacts/grid_evaluation.yaml`, plus `artifacts/registry_summary.yaml` (the one extra input; used only for `distance_to_profitable`). Minimal context.
