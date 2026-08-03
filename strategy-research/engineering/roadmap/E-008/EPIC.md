# E-008 — q1_26 tick archive aggregation

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-03

## Why

Kraken's `q1_26` tick archive (`Trades` — time-and-sales, not OHLCVT) is on
disk but not ingested: there is no aggregation path from trade-level ticks to
the OHLCVT bars the rest of the pipeline consumes. It sits alongside the G1
4,151-bar seam (Kraken's bulk OHLCVT archive ends 2025-12-31 23:00; the live
endpoint only reaches back ~173 days) as a possible way to help close that
gap, but nobody has built or evaluated the aggregator.
`trading-bot/data/data_manager.py:637` already contains a `.resample()` call
used today for aux-feed alignment (e.g. funding rate onto price interval) —
a plausible existing seam to extend, not yet evaluated for this purpose.

## Done when

A tick→OHLCVT aggregator exists, runs against the `q1_26` archive, and
produces bars whose values are verified against an independent reference
(e.g. Kraken's own published OHLCVT for an overlapping period, if one
exists, or a hand-computed check on a small window) — with a test asserting
the aggregation matches within a stated tolerance.

## Stories

- [ ] S1 — Evaluate `data_manager.py:637`'s existing `.resample()` seam:
      does extending it fit, or does trade-level aggregation need its own
      code path (volume-weighted OHLC construction is a different operation
      from resampling already-built bars)?
- [ ] S2 — Build the aggregator, with a correctness test against a known
      reference window.
- [ ] S3 — Run it against `q1_26`, register the resulting bars, and assess
      whether it helps close the G1 seam.

## Log

- 2026-08-03 — `new`. Written up in E-001 S4 (dispatch W24) from the HANDOFF
  ledger's q1_26/G1 notes. Not started.
