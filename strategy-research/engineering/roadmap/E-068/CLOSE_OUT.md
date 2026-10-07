# E-068 close-out (2026-10-07)

**Epic:** every run produces a proven finding and the next test to run (Linear project
P-CUL-76). **Status:** Completed. Design: `DESIGN_PROPOSAL.md`. Real runs: `VALIDATION_RUN.md`.

## What a run does now (with the flags on)

1. **Step 1a writes a claim card:** one sentence, its kind, and 1 to 3 tests composed from four
   slots (which bars, what happens next, compared with what, measured how). Code checks the card
   before anything is spent. A block idea needs a test that reads the block (CUL-409).
2. **Code measures the claim tests** after the backtests: effect sizes per variant and window,
   in `artifacts/claim_measurement.yaml` (renamed from `claim_status.yaml`; old runs still read).
   **Measured, not proven:** no verdict in the running pipeline (D-077). The verdict path of
   `tools/claim_tests.py` is kept and tested but parked (CUL-394).
3. **The run's finding** goes into campaign memory, with a summary later runs and readers see
   (D-072). A run that built an approximation of the idea says so first (D-075).
4. **Readers v3** see the claim, its measured numbers (each statistic labelled, CUL-413), the
   block manifest and the real settings. They explain the result and propose side findings
   only: each one a claim with its tests, optionally with a config change (D-073, D-078).
5. **Decide-next** turns a side finding into a candidate that starts from the source run's
   config (CUL-412, D-078). With approval mode on, every new pick waits for `--approve` (D-071).

## Against the objective's "done when"

| Item | Result |
|---|---|
| 1a writes the claim, its test and the rationale | Built (slice 2) |
| A review checks the test against a checklist | Code checks built; the model review **parked** (CUL-397: failed its offline gate) |
| The grid judges the claim on that test | **Changed by decision:** the claim is measured, not judged (D-077); automatic verdicts parked (CUL-394) |
| Readers see claim, manifest and settings; output findings and next tests | Built (slice 5, D-073, D-076, D-078) |
| Findings stored and retrievable | Built (slice 4, D-072); stored as measurements, not verdicts |

## Evidence from real runs (`VALIDATION_RUN.md`)

- run_070 to run_074 exercised the chain end to end. run_073 was the first run to reach the v3
  readers; run_074 kept a pre-filled claim and measured rank IC +0.054 at 1-4h, positive in 6 of
  6 windows. That is a measurement on one sample, not a validated edge.
- The last two validation runs cost $0.893 and $1.022.
- The blocking problems they showed were fixed: CUL-405/406 (PR #332), CUL-408/409/410
  (PR #334), CUL-412/413 (PRs #336, #337). Smaller ones are listed below as left open.

## Flags

Everything is off on master: `claim_tests`, `reader_findings`, `decide_next`, `nearest_build`,
`operator_approval`. Flag-off output is byte-identical, except for two changes declared in D-077:
the campaign summary's Requests section, and one path line in `campaign_knowledge_base.yaml`.

## Pull requests

#311 and #317 (design), #315 and #316 (slice 1), #318 (1b), #319 (slice 2), #320 (slice 3),
#323, #324, #326, #327, #328 (slice 4), #329 (slice 5), #330, #332, #333, #334, #335 (plan),
#336 (D-078), #337 (D-077); validation reports #322, #325, #331.

## Left open (Backlog in the project)

| Ticket | What |
|---|---|
| CUL-394 | Automatic claim verdicts (calibration store, hourly gate) -- parked |
| CUL-397 | The model review of a claim's tests -- parked |
| CUL-391 | A calibrated significance method for regime selectors |
| CUL-383 | Re-grade reader patches on fresh windows, or accept the same windows (decision) |
| CUL-387 | Re-grade run_066: the recomputed signal does not match the traded one |
| CUL-392 | Multi-card split siblings skip step 1b |
| CUL-404 | Warn-only schema mismatches on real cards |
| CUL-407 | Component request: candle-shape inputs |
| CUL-347 | C2 S2e follow-ups |

## Held for the operator

`component_attribution-run_071-1` and `trade_efficiency-run_073-1` are
`blocked_on_operator_approval` in the main checkout's queue. With PR #336 merged, they can be
approved (`run_campaign.py --approve <id>`) or left held. No campaign was launched at close-out.
