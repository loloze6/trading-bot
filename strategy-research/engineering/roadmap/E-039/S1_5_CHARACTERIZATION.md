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

**2. The timeframe-derivation trap — flagged as HIGH RISK for the next
implementer, verified partially, not fully resolved.**

This project's own architecture notes record, as a verified fact
(2026-08-27): a 4-hour backtest is expected to run off the existing 1-hour
cache file when no 4-hour file exists — the engine aggregates finer cached
data up to the requested timeframe during the run. This is real, documented
behavior, not a hypothesis (an earlier bug already happened from getting this
wrong once — a stale doc comment caused a redundant re-fetch when it assumed
the source was "live ticks" instead of a finer cache).

**Checked directly in this session:** the fetcher `check_data.py` calls
resolves its cache filename from the *exact* requested timeframe —
`CcxtFetcher.cache_key()` returns `f"{symbol}_{ccxt_timeframe}"` (e.g.
`BTCUSDT_4h`), snapped from `candle_interval_seconds`. It does **not** know
about the "derive from a finer cache" behavior described above. So: **as
currently written, `check_data_availability("4h", ...)` would look for a file
literally named `BTCUSDT_4h` and could report "no data" for a variant the
real engine would run perfectly fine off `BTCUSDT_1h.csv`.** That is a false
decline — the exact trap Jérémy flagged.

**What I did NOT find, in a time-boxed search this session:** the exact code
path that performs the real derivation (which module decides "read the finer
cache and aggregate" during an actual backtest run). It is not a simple
"prefer the finer cache_key" branch in the fetcher — I checked `cache_key()`,
`_load_local()`, and `DataManager`'s aux-feed resampling path, and none of
them is it. It most likely lives in how the backtest replay loop selects
which raw rows to feed `CandleBuilder` (which does the actual aggregation,
row by row, elsewhere in `data_manager.py`), but this was not pinned to a
specific file:line before this document was written.

**Consequence for whoever builds S1.5: do not wire `check_data.py` in as-is.**
Before this check can be trusted, someone must:
(a) find and read the exact code path that performs finer-to-coarser
derivation in a real backtest run, then
(b) either extend the feasibility check to replicate that same
derivation logic when deciding what counts as "available" (checking for
a finer existing cache before declaring a coarser one missing), or
(c) confirm no such extension is needed because the derivation happens at
a layer this check doesn't need to duplicate.
Skipping this step means the very first real use of S1.5 risks silently
declining variants that were always feasible — worse than doing nothing,
because it would look authoritative while being wrong.

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
