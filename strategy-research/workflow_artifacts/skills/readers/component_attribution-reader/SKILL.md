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
Read this run's own `component_attribution.yaml` report (nothing else) and propose zero or
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

**Scope boundary.** Same as every other reader in this family: no other category's
`reports/*.yaml`, no `verdict_interpretation.yaml`, no raw `bars.csv` directly (this report
already extracted the `debug_info.components.*` columns for you), no `fragment_patterns.yaml`.

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
`rubric_version: "component_attribution-reader-v1"`. `kind: patch` is expected to dominate
here (tuning an existing component's `weight`/`scaling_factor`/threshold per
`STRATEGY_DESIGN_GUIDE.md`'s "Component variant patterns"); `kind: new_block` applies only
when the evidence shows an existing component's regime-conditional behavior that NO current
component captures well (see Rule CA-2 below).

**Patch item shape (required, `proposal.schema.json`):** every item of a `patch` list is
exactly `{component_id, field, before, after}` -- `field` is the dotted path of the changed
parameter inside that component (e.g. `transforms[2].params.min_abs`). `tools/reader_proposals.py` rejects a patch item
without it, which stops the pipeline. A `new_block`'s `block.config_paths` must list at least one path.

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
`STRATEGY_DESIGN_GUIDE.md`'s regime-block pattern: components differ per regime already, per
`strategies.regimes.<regime>.components`) -- or a `new_block` sketch if the divergence suggests
a genuinely new, regime-specific component would capture the pattern better than tuning the
existing one.
*Justification:* this project's regime-gate architecture already assumes components can
differ by regime (`STRATEGY_DESIGN_GUIDE.md` §"Ungated hypotheses"/worked example) -- a
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

| Score | `confidence_real` | `distance_to_profitable` | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `variants.base.slices.overall` is unavailable (no `debug_info.components.*` columns anywhere), or the pattern rests on a component with constant aggregate output (Rule CA-1) or cross-window inconsistency (Rule CA-3). | No profitability-adjacent framing is possible from this report alone (it carries no PnL/cost fields) -- `distance_to_profitable` can only be inferred indirectly via mechanism plausibility; default to 0 unless a clear regime-divergence pattern (CA-2) suggests a specific, nameable fix. | The divergence/degeneracy appears in exactly one window's aggregate with no corroboration elsewhere. |
| 1 | Evidence from a single window's `per_window` aggregate only, no `per_regime`/`per_symbol` corroboration of the same component. | A CA-2 divergence exists but the magnitude is marginal (`mean`/`median` differ but not obviously "on" vs "off" between regimes). | Pattern recurs in 2 aggregate groups (windows or regimes) for the same component, no third corroborating grouping. |
| 2 | `variants.base.slices.per_regime` shows the same divergence pattern for a component across 2+ regime labels' aggregates, consistently. | CA-2 divergence is clear (near-zero/constant `mean`/`median` in one regime, clearly nonzero with a real `p10`-`p90` spread in another) suggesting a plausible, specific `patch` (e.g. zero the component's weight in the inert regime). | Pattern recurs across 3+ aggregate groups (windows/regimes/symbols) for the same component. |
| 3 | The same component's divergence pattern holds across `per_window`, `per_regime`, AND `per_symbol` aggregates simultaneously, with `components_discovered` confirming consistent presence across all windows (ruling out CA-3). | CA-2 divergence maps directly onto an existing config lever this project's `STRATEGY_DESIGN_GUIDE.md` already documents (e.g. a regime-specific component list, or a documented scaling_factor/weight pattern) -- the fix is a small, well-precedented `patch`, not speculative. | Corroborated across `per_window`, `per_regime`, AND `per_symbol` for the same component, with a stated causal story (e.g. "component X's signal is regime-specific by design intent -- its near-zero aggregate outside trending is consistent, not broken -- so the proposal narrows its weight to the regime where it demonstrably varies"). |

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
  `STRATEGY_DESIGN_GUIDE.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/component_attribution.yaml` and, if present,
`artifacts/grid_evaluation.yaml`. Minimal context.
