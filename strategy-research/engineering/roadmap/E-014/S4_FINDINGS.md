# E-014 S4 — Refuse untradable/unpriceable briefs at registration: characterization (CUL-183)

**Date:** 2026-09-03
**Status:** characterize-and-STOP. No code changed. Report, then stop for
Jérémy's/Dorian's go-ahead on the actual refusal change.

## What already exists (confirmed, not assumed)

`workflow/run_campaign.py::_materialize_run` (line ~288) already:
- Requires `venue`/`product`/`strategy_domain`/`market_universe`/`timeframe`/
  `research_goal` in the brief's frontmatter — `_parse_brief_frontmatter`
  raises outright if any is missing, at registration time.
- Computes `research_only = not _venue_product_tradable(venue, product)` and
  writes it into `research_brief.yaml` — also at registration time, from the
  same `config/venue_tradability.yaml` table CUL-183 wants used.

**What's actually missing is narrower than "build a check":** the check and
the data are already both there and already run early. What's missing is
that an **untradable** result doesn't refuse anything — it just sets
`research_only=True` and lets the entire pipeline (hypothesis generation
through a full walk-forward backtest) run anyway, deferring the actual
refusal to stage 13 (`_route_holdout_evaluation`, which checks
`research_only is not False` right before the single-use holdout). CUL-183's
real ask is moving the **refusal**, not the **check** — the check already
moved.

## Q1: How many briefs would an early gate have refused?

**Measured, not estimated:** `grep -l research_only runs/*/artifacts/research_brief.yaml`
→ **1 of 58** run directories carries the field at all (the rest predate
E-015 S1b, 2026-08-20, which introduced it). Of that one, its value would
need checking individually to know if it's `true`/`false`, but the headline
number matters more: **an early gate would have had essentially nothing to
retroactively refuse**, because the corpus overwhelmingly predates the
concept of a declared venue/product. This matches CUL-183's own "0 of 57"
figure almost exactly (58 vs 57 — one more run happened since that ticket
was filed, on the new registration path).

**Consequence for the backfill-vs-grandfather question:** it's close to
moot. There is no meaningful backlog of in-flight, non-compliant briefs to
grandfather — briefs materialize and run roughly one at a time, not as a
large pre-existing queue, and `_parse_brief_frontmatter` already hard-fails
any NEW brief missing venue/product today. The only real decision is what
happens to the **historical** 57 run directories' records if anything ever
needs to re-derive their tradability after the fact (e.g. for reporting) —
and nothing found in this pass suggests anything currently depends on that.

## Q2: Has `component_gap` (stage 6) ever actually fired?

**Yes — exactly once, and it worked as intended.** `run_057`'s
`backtest_spec.yaml` shows a real `component_gap` episode:

1. `operator_correction_20260710`: a wired ER-gate implementation was found
   to re-evaluate every bar via regime dispatch (a trailing stop) instead of
   the brief's intended entry-only latch — routed to `component_gap` because
   the engine's existing components could not express the intended
   semantics.
2. `operator_resolution_20260711`: resolved by building a new component
   (`GatedSmaTrendLongOnlyComponent`, `trading-bot/strategies/strategy_components.py`)
   with proper latch semantics, verified by **30/30 gate-disabled bar-for-bar
   forecast equivalence** against `run_054`'s canonical results plus two
   synthetic fixtures, before `status` was updated from `component_gap` to
   `spec_ready`.

The other ~42 files matching a `component_gap` grep all carry the field as a
schema-required key defaulting to `null`/absent — not an actual firing. Only
`run_057` shows a real value and a real resolution.

**This is a good sign for E-033 D4's assignment** (implementation
feasibility belongs to `refinement_planner`, not this epic): the one real
`component_gap` case was resolved competently, with real verification, by
the existing mechanism — there's no evidence this gate is broken or
under-used, just rare.

## Net assessment

CUL-183's own framing ("verified 2026-09-01: the information is present at
the right moment today; only the refusal is missing") is confirmed exactly
by this pass, with numbers behind it now instead of an unverified claim:

- The check and its data source already exist and already run at
  registration (`_materialize_run`).
- Historical impact of adding the refusal is ~zero (1 of 58 briefs even
  carries the field; no meaningful grandfathering problem).
- The adjacent mechanism this ticket explicitly leaves alone
  (`component_gap`, stage 6) is proven working on its one real test case.

**The actual change, when built, is small:** turn `_materialize_run`'s
`research_only = not tradable` computation into a hard refusal (raise, name
the venue/product and the reason) when `tradable` is `False`, mirroring
`_parse_brief_frontmatter`'s existing fail-loud pattern for missing fields —
not a new mechanism, an extension of one already in the same function. The
stage-13 gate stays exactly as-is, as CUL-183 already specifies (last line
of defense before the holdout, not an alternative to the early one).

Nothing built in this pass. Reporting and stopping per CUL-183's own
instruction.
