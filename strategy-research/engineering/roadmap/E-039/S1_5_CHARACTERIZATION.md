# E-039 S1.5 — Pre-backtest implementation-feasibility check: characterization

**Date:** 2026-09-02
**Status:** characterize-and-STOP. Two decisions made by Jérémy (A, B below).
Two more things flagged that are NOT decided and NOT safe to assume — read
"Open, unresolved" before writing any code.

## What already exists

`tools/check_data.py::check_data_availability(symbols, start, end, timeframe)`
already does a version of this check. It calls the real
`DataManager.fetch_historical_data()` path — the same call `protocol_execution`'s
engine uses — for each symbol across a requested window, and flags an empty
return or any gap exceeding ~2 candle-intervals. It is currently CLI-only
(`python check_data.py --protocol <file>`), invoked by nobody in the pipeline.
This is a mechanism to reuse as a starting point — **not** a drop-in solution;
see "Open, unresolved" below for why it cannot be wired in as-is.

## Where the input lives

Each run's protocol is a per-run generated JSON file (e.g.
`protocols/run_050_generated.json`), referenced by `run_context.yaml`'s
`protocol` field, declaring `symbols`, `timeframe`, and `windows` (each
`{label, test: {start, end}}`). Confirmed directly on `run_050`: 76 windows,
symbols `["BTCUSDT", "ETHUSDT"]`, timeframe `1h`, earliest window
`2019-09-01`. This file exists before `protocol_execution` runs.

A variant's config (`candidate_strategy_config.json`) can also declare
`aux_feeds` (e.g. funding rate, fear/greed, whale flows) alongside the
`strategies`/`regime_detector` blocks — confirmed by inspecting a real run's
config. **Scope correction (Jérémy, 2026-09-02): the feasibility check must
cover every data series the variant needs, not price alone** — an aux feed
that doesn't exist for the requested venue/window is exactly as fatal as a
missing price cache, and today nothing checks it before the engine runs.

## Where the crash happens today

`protocol_execution` (a tool stage, no LLM) invokes the real engine once per
window. CUL-230 traced one crash mechanism: an interior data gap combined
with a failed optional gap-fill (network/rate-limit) fell through to an empty
frame instead of the cached rows — fixed 2026-09-02 (PR #109,
`tolerate_fill_failure`). That fix makes the engine more tolerant of a
transient fetch failure; it does not stop a genuinely infeasible window (no
data at all for a symbol/feed/period) from reaching the engine in the first
place. Nothing today checks feasibility before invoking the engine.

## Scope boundary — restated, because it is easy to over-widen

S1.5 is a **hard, mechanical, data-only** check: for the symbols, timeframe,
window, and aux feeds a variant declares, does the data exist (or can it be
correctly derived — see "Open, unresolved" #2)? It answers a yes/no/partial
question with one right answer, never a guess.

**Explicitly out of scope, on purpose:** whether a new indicator/component is
*possible to build*, and at what engineering cost. That is a judgment call,
not a fact-check, and it already has an owner: E-033 D4 assigns
implementation feasibility to `refinement_planner`, specifically because A8.6
was killed for being exactly this kind of soft, guessed check dressed up as a
gate. Folding indicator-buildability into S1.5 would recreate the problem
A8.6's removal was meant to solve. If that assignment should change, that is
its own decision revisiting E-033 D4 — not something to slide into S1.5
quietly.

## Outcome model (Jérémy, 2026-09-02)

Every variant gets exactly one of three outcomes from this check:

- **Validate** — every data series the variant needs (price, every declared
  aux feed) is fully available for the whole requested window, within the
  acceptable-missing threshold (see "Open, unresolved" #1). Proceeds to
  `protocol_execution` unchanged.
- **Refine** — some of what's needed exists, but not all of it, in a way that
  can be worked around by narrowing the variant. Examples: price data covers
  2020–2026 but the variant asked for 2018–2026 (narrow the window); a
  funding-rate feed only starts in 2021 (drop it or narrow the window);
  a handful of specific months are missing entirely out of a 76-window
  protocol (drop those windows, keep the rest). Routes back with a stated
  reason and which window(s)/series are the problem — never a bare "no."
- **Decline** — a required series does not exist at all, for any window, at
  any granularity that could be derived (e.g. a symbol never tracked on this
  venue, or a feed that was never built). No workaround exists; the variant
  cannot run as specified.

## Decisions made (Jérémy, 2026-09-02)

**A — Build this as a real pipeline stage**, not a check bolted inline into
existing routing. A real `STAGE_CONFIGS` entry gets a handoff template, an
audit-log entry, and retry semantics for free, matching every other tool
stage (`signal_prescreen`, `protocol_execution`). An inline check would be a
second place besides `STAGE_CONFIGS` where routing logic lives — the exact
class of bug E-033 S1 already found once (`validation`'s `conditions` field
never reaching `backtest_specification` because the routing/handoff contract
didn't carry it).

**B — Check every window individually**, not the full protocol span in one
call. This is what makes "refine" possible at all: a whole-span check can
only ever say "something in here is missing," never *which* window or *why*
— and "refine" requires knowing which windows are the problem so the variant
can be narrowed around them rather than declined outright.

## Open, unresolved — do not assume either of these

**1. What counts as "acceptable missing"?** A trigger of "100% of the data
must exist" would decline almost every variant in practice — real caches
have small gaps everywhere. `check_data.py`'s existing ~2-candle-interval gap
tolerance was tuned for a different purpose (basic sanity-checking a fixed
protocol) and has never been evaluated as a feasibility threshold. This needs
its own explicit, deliberately-chosen number (e.g. "more than X% of expected
bars missing in a window → refine, not validate") — pre-registered like every
other threshold in this project, not inherited by accident from an unrelated
tool. **Not decided. Needs its own pass before building.**

**2. The timeframe-derivation trap — RESOLVED (conclusively, not partially):
the claimed capability does not exist. Filed as CUL-250.**

This project's architecture notes used to claim, as a "verified" fact: a
4-hour backtest runs off an existing 1-hour cache file when no 4-hour file
exists — the engine aggregates finer cached data up to the requested
timeframe during the run. **That claim was false, and is now corrected** in
`CLAUDE.md` (2026-09-03).

**Code trace (complete, not partial):** `CcxtFetcher.cache_key()` returns
`f"{symbol}_{ccxt_timeframe}"` — fetch and cache lookup happen at the exact
requested timeframe. `DataManager.__init__` passes the SAME `interval_seconds`
to both the fetcher and `CandleBuilder` — there is no split between "fetch
finer, aggregate coarser." `CandleBuilder.add_row()` aggregates whatever rows
it's given; when those rows are already at the target interval, aggregation
is a no-op. Checked every candidate site — `cache_key()`, `_load_local()`,
`_load_all()`, `CandleBuilder.__init__`/`add_row`, `DataManager.__init__`,
and a repo-wide grep for `resample`/`coarser`/`finer` across `trading-bot/` —
none of them derives a coarser timeframe from a finer cache.

**Live-reproduced, not just traced:** re-ran `run_060`'s actual protocol
(4h timeframe) through the real engine after the CUL-230 fetch fix (PR #109)
shipped. It still crashed at window 2020-02, because `BTCUSDT_4h.csv`
genuinely stops at 2020-02-01 while `BTCUSDT_1h.csv` is ~99% complete for the
same period — the data exists, the engine just never looks for it under a
different timeframe name.

**This exact gap was already found and fixed once — in a bypass tool, not
the engine.** `strategy-research/tools/prescreen_signal.py::_resolve_ohlcv_source`
(added 2026-08-28, docstring cites `run_060` as the trigger) already
implements coarsest-evenly-dividing-finer-cache resolution + resample. Its
docstring claimed "the engine has never had this problem" — an unverified
assumption, now corrected in that file too (2026-09-03).

**Consequence for whoever builds S1.5: do not wire `check_data.py` in as-is
until CUL-250 is fixed or explicitly deferred.** `check_data_availability`
would falsely decline a variant needing 4h data when only 1h exists, exactly
as this section originally warned — the warning was right, the underlying
capability just turned out not to exist rather than being merely undocumented.
CUL-250 proposes porting `prescreen_signal.py`'s proven pattern into
`CcxtFetcher`; once that ships, S1.5 can rely on `check_data_availability`
(or an equivalent check) reflecting reality. Until then, S1.5 must either
wait on CUL-250, or independently replicate the same coarsest-dividing-cache
resolution `prescreen_signal.py` already proves works.

## Verification method before this becomes a blocking gate

Once the above two open points are resolved, run the check against all 7 of
S1's re-scored runs (`run_043, 044, 047, 048, 050, 053, 060`) plus 3-5 healthy
control runs from the corpus, and confirm:

- It correctly flags `run_050` and `run_060` — the two that actually crashed.
- It does **not** flag any of the 5 that completed successfully, or any
  healthy control run — a false positive here would silently block
  legitimate research, which is worse than the problem S1.5 exists to fix.
- It does **not** flag any run whose timeframe is coarser than its cache file
  but derivable from a finer one (see the trap above) — a dedicated test case
  for this must be constructed, not assumed to be covered by the corpus.

Only after that measurement passes should S1.5 move from "characterized" to
"built and wired as a gate."
