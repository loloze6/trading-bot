# E-039 S1.5 — Pre-backtest implementation-feasibility check: characterization

**Date:** 2026-09-02
**Status:** characterize-and-STOP — no code changes made. Two design questions below need Jérémy's call before building.

## What already exists

`tools/check_data.py::check_data_availability(symbols, start, end, timeframe)`
already does exactly the check S1.5 asks for. It calls the real
`DataManager.fetch_historical_data()` path — the same call `protocol_execution`'s
engine uses — for each symbol across the full requested window, and flags an
empty return or any gap exceeding ~2 candle-intervals. It is currently CLI-only
(`python check_data.py --protocol <file>`), invoked by nobody in the pipeline.
This is the mechanism to reuse, not reinvent.

## Where the input lives

Each run's protocol is a per-run generated JSON file (e.g.
`protocols/run_050_generated.json`), referenced by `run_context.yaml`'s
`protocol` field, declaring `symbols`, `timeframe`, and `windows` (each
`{label, test: {start, end}}`). Confirmed directly on `run_050`: 76 windows,
symbols `["BTCUSDT", "ETHUSDT"]`, timeframe `1h`, earliest window
`2019-09-01`. This file exists before `protocol_execution` runs — it is
produced earlier in the pipeline and is exactly the artifact `check_data.py`
already knows how to read (`--protocol` mode reads this same shape).

## Where the crash happens today

`protocol_execution` (a tool stage, no LLM) invokes the real engine once per
window. CUL-230 traced the crash mechanism: an interior data gap combined with
a failed optional gap-fill (network/rate-limit) fell through to an empty
frame instead of the cached rows — fixed 2026-09-02 (PR #109,
`tolerate_fill_failure`). But that fix makes the ENGINE more tolerant of a
transient fetch failure; it does not stop a genuinely infeasible window
(no data available at all for a symbol/period) from reaching the engine in
the first place. Nothing today checks feasibility before invoking the engine —
which is exactly Jérémy's original point.

## Proposed S1.5 mechanism

1. A check between `backtest_specification`'s routing decision and
   `protocol_execution`'s invocation.
2. Reads the run's protocol file — the same one `protocol_execution` will use.
3. Calls `check_data_availability(symbols, start, end, timeframe)` (reused,
   not rewritten) against the window span the protocol declares. No LLM,
   deterministic, cheap relative to the backtest itself.
4. **PASS** → proceeds to `protocol_execution` unchanged, byte-identical to
   today's behavior for every protocol this check would pass.
5. **FAIL** (gap or empty return) → writes a `feasibility_result.yaml`
   (status: infeasible, which symbol/window, why) and routes to **refine**,
   never to a silent crash and never to a silent skip — matching Jérémy's
   framing exactly: *"always backtest a variant that can be backtested."*

## Two open design questions — Jérémy's call, not built here

**A. New pipeline stage vs. an inline check inside existing routing.**
A real `STAGE_CONFIGS` entry gets a handoff template, an audit-log entry, and
retry semantics for free, matching the house pattern every other tool stage
(`signal_prescreen`, `protocol_execution`) already follows. An inline check
bolted into the existing `backtest_specification -> protocol_execution`
routing is cheaper to add but creates a second place besides `STAGE_CONFIGS`
where routing logic lives — which is the exact class of bug E-033 S1 already
found once (`validation`'s `conditions` field never reaching
`backtest_specification` because the routing/handoff contract didn't carry
it). **Recommendation: a real stage**, for that reason — but it's a
recommendation, not a decision made here.

**B. Check the full protocol span, or every window individually?**
Checking the FULL span (earliest window start to latest window end) in one
call is simplest and matches what "can this protocol run at all" means, but a
76-window protocol spanning 2019-2026 (like `run_050`'s) fails entirely if
even one month anywhere is bad — even though 75 of 76 windows might be fine.
Checking PER WINDOW is more precise and matches the "reject or refine THIS
variant" framing at a finer grain, but multiplies the number of
`check_data_availability` calls by the window count (76x for `run_050`'s
shape). Each call does a real data fetch, so the cost difference should be
**measured**, not assumed, before choosing — this is exactly the kind of
claim S1's own findings already flagged as needing evidence, not instinct.

## Verification method before this becomes a blocking gate

Run the check (whichever grain B decides) against all 7 of S1's re-scored
runs (`run_043, 044, 047, 048, 050, 053, 060`) plus 3-5 healthy control runs
from the corpus, and confirm:

- It correctly flags `run_050` and `run_060` — the two that actually crashed.
- It does **not** flag any of the 5 that completed successfully, or any
  healthy control run — a false positive here would silently block
  legitimate research, which is worse than the problem S1.5 exists to fix.

Only after that measurement passes should S1.5 move from "characterized" to
"built and wired as a gate."

## Relationship to A8.6 and E-033 D4 (restating, for the record)

This is deliberately narrower than both precedents it is sometimes confused
with:

- **A8.6** (removed) was a *soft, guessed* judgment call about whether a
  strategy would activate — not reproducible, not mechanical. S1.5 is a hard
  yes/no fact about data that already exists on disk.
- **E-033 D4** (implementation feasibility, owned by `refinement_planner`) is
  about whether the *strategy logic* can be expressed by the engine's
  components. S1.5 is about whether the *data* for the requested
  symbols/timeframe/window can be assembled at all. They are independent
  checks and neither substitutes for the other.
