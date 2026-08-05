# E-014 — Venue-parameterized cost model + calibration re-runs

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §1.2, verbatim: "**Venue-parameterized cost model +
calibration re-runs.** Objective: backtests price the venue we'd actually
use. Deliverable: the cost model takes the venue's real fee schedule (incl.
maker-order assumptions where realistic); then **3 automated calibration
re-runs** of already-tested ideas (the funding retest + 2 archived
near-misses) under the new fee model — objective of these runs: measure how
much verdicts move on fees alone, i.e. how many 'kills' were venue
artifacts."

Dependency on E-010 (slippage and lot-size/min-notional model): E-010's
Done-when requires fee and slippage drag to be attributed *separately* in the
run artifact — that seam is what E-014 plugs a real venue fee schedule into.
Building E-014 before E-010 lands means building the fee/slippage split
twice, and re-baselining every pinned hash (e.g. E-010's
`config_sha`/`data_sha` pins) twice. E-014 follows E-010.

## Done when

1. The cost model takes a venue-specific fee schedule as a parameter (not the
   current hardcoded 10 bps fee), including maker-order assumptions where
   realistic for the decided venue.
2. Three automated calibration re-runs execute under the new fee model: the
   funding retest and the 2 archived near-misses named in the source text.
3. For each of the 3 re-runs, the verdict movement attributable to fees alone
   is measured and recorded — i.e., which of the original kills were venue
   artifacts (would have passed under the new fee schedule) and which were
   not.

## Stories

- [ ] S1 — (blocked behind E-010) Parameterize the cost model by venue fee
      schedule, building on E-010's fee/slippage attribution seam in the run
      artifact.
- [ ] S2 — Run the 3 calibration re-runs (funding retest + 2 archived
      near-misses) under the new fee model; record verdict deltas
      attributable to fees alone.

## Log

- 2026-08-05 — `new`. Created from E-013 S1's audit of `docs/ROADMAP.md` §1.2
  (dispatch W35). Dependency on E-010 recorded per the audit's sequencing
  finding; not started.
