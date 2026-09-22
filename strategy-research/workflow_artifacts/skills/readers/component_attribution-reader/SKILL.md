---
name: component_attribution-reader
description: Reads artifacts/reports/component_attribution.yaml (Slice 5a) plus
  artifacts/grid_evaluation.yaml (E-046b, when present) and proposes evidence-grounded
  patch/new_block candidates to artifacts/proposals/component_attribution.yaml. One of 5
  specialist readers replacing verdict-interpreter/SKILL.md's monolithic context (E-046a
  Slice 5b-i). Unlike the other 4 readers, this category has NO existing rule-block analog in
  verdict-interpreter/SKILL.md -- its rules below are new content, authored for this build
  (see "Rules" section's own reasoning). Does NOT decide hypothesis_verdict/lineage_routing/
  status -- that authority stays with the not-yet-built mechanical verdict-synthesis step
  (5b-ii; see S1_FINDINGS.md's "Decision" section, 2026-09-22).
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
```yaml
category: component_attribution
slices:
  overall:
    components_discovered: [<name>, ...]   # sorted list of component names found in ANY
                                            # window's bars.csv debug_info.components.* columns
                                            # -- inventory only, zero aggregation.
    note: "inventory only ... see per_window for the raw per-bar values."
    # OR {unavailable: true, reason: "..."} when no debug_info.components.*.* columns exist
    # in any window's bars.csv for this run.
  per_window:   # {window_label: [{symbol, window, timestamp, regime, component, <metric>: <value>, ...}, ...]}
                # one record per (bar, component) pair, raw per-bar values -- NOT aggregated.
  per_regime:   # {regime_label: [same record shape]} -- excludes the trailing blank-regime
                # boundary row (build_reports.py's own CODE-REVIEW FIX, 2026-09-21).
  per_symbol:   # {symbol: [same record shape]}
```
Every record is one component's raw per-bar debug output (whatever metric columns that
component's `debug_info.components.<name>.*` emitted -- field names are component-specific
and not fixed ahead of time). There is no pre-computed aggregate anywhere in this report;
any statistic you cite (e.g. "mostly zero," "varies by regime") must be something you can
point to directly in the listed records, not an inferred summary you cannot show your work for.

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

### `evidence` format rule
```yaml
# GOOD
evidence:
  - "slices.overall.components_discovered=['rsi','keltner']; slices.per_regime.trending
     records for component='keltner' show non-zero varying values across 40+ bars, while
     slices.per_regime.mean_reversion records for the same component are constant 0.0 across
     every bar listed -- keltner appears inert outside trending."

# BAD
evidence:
  - "The keltner component isn't contributing much."
```

## Rules (new territory -- authored for this reader; no existing analog in
verdict-interpreter/SKILL.md)

**RULE CA-1 — Degenerate/constant output is not evidence-worthy on its own:**
If a component's per-bar values in `slices.per_window[<window>]` are constant (e.g. always
`0`, always the empty string, or always the same value) across an ENTIRE window's records,
that component is dead in that window -- not tunable via a parameter `patch` in that window.
Do not propose a `patch` adjusting `weight`/`scaling_factor` for a component that shows no
variation to tune in the first place; flag it in `evidence` as a wiring/config concern instead
(e.g. "component X emits a constant 0.0 across all N records in window Y -- likely gated off
or misconfigured, not a tuning target"), and keep `confidence_real` low unless the same
constant-output pattern recurs consistently enough to be a genuine, reportable finding rather
than a proposal.
*Justification:* a component with zero observed variation offers no basis to judge which
direction a `weight`/`scaling_factor` change would even push it -- proposing a tuning patch on
constant data is unfalsifiable by construction.

**RULE CA-2 — Regime-conditional divergence IS evidence-worthy:**
If a component's records in `slices.per_regime` show a materially different range or central
tendency across regime labels (e.g. non-trivial, varying values in one regime's record group,
near-constant/near-zero in another), that divergence is evidence-worthy. Propose a `patch`
adjusting that component's `weight` or a regime-specific parameter if the config already
supports per-regime component sets (per `STRATEGY_DESIGN_GUIDE.md`'s regime-block pattern:
components differ per regime already, per `strategies.regimes.<regime>.components`) -- or a
`new_block` sketch if the divergence suggests a genuinely new, regime-specific component
would capture the pattern better than tuning the existing one.
*Justification:* this project's regime-gate architecture already assumes components can
differ by regime (`STRATEGY_DESIGN_GUIDE.md` §"Ungated hypotheses"/worked example) -- a
component behaving differently across regimes in the RAW per-bar data is the most direct
component-level signal this report can offer that a regime-specific config change is worth
proposing, without needing any cross-category (profitability/pnl) evidence to justify it.

**RULE CA-3 — Cross-window inconsistency in `components_discovered` is informational, not a
tuning proposal:**
If a component name appears in some windows' bars.csv (and thus in the per-window/per-regime
records) but is absent from others within the SAME run, note this explicitly in `evidence` as
a possible wiring/config inconsistency (e.g. a component conditionally emitted, or a config
that changed between windows) rather than silently proposing a tuning patch on top of
possibly-inconsistent data. Keep `confidence_real` at 0-1 for any proposal touching that
component until the inconsistency itself is understood.
*Justification:* per-bar attribution built on a component that isn't even consistently present
across this run's own windows cannot support a confident tuning claim -- the inconsistency
itself is more informative than any pattern built on top of it, and reporting it as a finding
(even with no proposal attached) is more honest than papering over it with an average.

If none of CA-1/CA-2/CA-3 identify a genuine pattern in this report, do not force a proposal.

## Scoring (0-3 anchors)

**Do not free-hand these three scores.**

| Score | `confidence_real` | `distance_to_profitable` | `mechanism_plausibility` |
|---|---|---|---|
| 0 | `slices.overall` is unavailable (no `debug_info.components.*` columns anywhere), or the pattern rests on a component with constant output (Rule CA-1) or cross-window inconsistency (Rule CA-3). | No profitability-adjacent framing is possible from this report alone (it carries no PnL/cost fields) -- `distance_to_profitable` can only be inferred indirectly via mechanism plausibility; default to 0 unless a clear regime-divergence pattern (CA-2) suggests a specific, nameable fix. | The divergence/degeneracy appears in exactly one window's records with no corroboration elsewhere. |
| 1 | Evidence from a single window's `per_window` group only, no `per_regime`/`per_symbol` corroboration of the same component. | A CA-2 divergence exists but the magnitude is marginal (values differ but not obviously "on" vs "off" between regimes). | Pattern recurs in 2 record groups (windows or regimes) for the same component, no third corroborating grouping. |
| 2 | `slices.per_regime` shows the same divergence pattern for a component across 2+ regime labels' record groups, consistently. | CA-2 divergence is clear (near-zero/constant in one regime, clearly varying in another) suggesting a plausible, specific `patch` (e.g. zero the component's weight in the inert regime). | Pattern recurs across 3+ record groups (windows/regimes/symbols) for the same component. |
| 3 | The same component's divergence pattern holds across `per_window`, `per_regime`, AND `per_symbol` simultaneously, with `components_discovered` confirming consistent presence across all windows (ruling out CA-3). | CA-2 divergence maps directly onto an existing config lever this project's `STRATEGY_DESIGN_GUIDE.md` already documents (e.g. a regime-specific component list, or a documented scaling_factor/weight pattern) -- the fix is a small, well-precedented `patch`, not speculative. | Corroborated across `per_window`, `per_regime`, AND `per_symbol` for the same component, with a stated causal story (e.g. "component X's signal is regime-specific by design intent -- it firing near-zero outside trending is consistent, not broken -- so the proposal narrows its weight to the regime where it demonstrably varies"). |

## Checklist
- Confirm variation exists (Rule CA-1) before proposing any tuning `patch`.
- Confirm the component's presence is consistent across this run's windows (Rule CA-3) before
  building confidence on a cross-window pattern.
- Every `evidence` entry cites a `slices.*` record (component name + field/value) from THIS
  report -- never an inferred aggregate you cannot point to directly.

## Forbidden
- Do not read or cite `reports/profitability.yaml`, `reports/trade_efficiency.yaml`,
  `reports/forecast_power.yaml`, `reports/regime_power.yaml`, `verdict_interpretation.yaml`,
  raw `bars.csv`, or `fragment_patterns.yaml`.
- Do not emit `hypothesis_verdict`/`lineage_routing`/`status`/`promote`/`kill`/`refine`/
  `pivot`/`escalate` anywhere in `proposals/component_attribution.yaml`.
- Do not propose a tuning `patch` for a component whose observed values are constant across
  the window(s) cited (Rule CA-1) -- there is nothing to tune toward.
- Do not compute or assert a statistic (mean, correlation, "mostly zero") you cannot show
  directly in the listed per-bar records -- this report performs zero aggregation by design;
  neither should you invent one silently.
- Do not invent component classes, transform ops, or regime names absent from
  `STRATEGY_DESIGN_GUIDE.md`.
- Do not emit a proposal with empty `evidence`.

## Context rule
Read only `artifacts/reports/component_attribution.yaml` and, if present,
`artifacts/grid_evaluation.yaml`. Minimal context.
