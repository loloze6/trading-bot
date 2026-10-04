# Amendment 5: the calibration gate becomes one-sided

Written and committed 2026-10-03, **before the code that applies it, before
the re-evaluated calibration summary, and before any run_065 effect size or
verdict is computed.** Operator decision of 2026-10-03 (DESIGN_PROPOSAL.md
section 3.1, PR #317). It amends amendment 3 section 5 (the pass rule) only.
Everything else stands: the gate's measurement, the verdict rule, the
operator rules, the pre-registered spec, the lock's scope rule (D-064) and
amendment 4's "not graded" rule.

## 1. The change

On no-edge prices, per row (model x side x direction), at every horizon:

| Share of p < 0.05 among defined p | Before (two-sided) | Now (one-sided) |
|---|---|---|
| above 0.075 (the ceiling) | fail | **fail, mandatory** |
| 0.025 to 0.075 | pass | pass |
| below 0.025 (the floor) | fail | **pass, with a warning: "conservative"** |

- "No answer" (undefined p) in more than 5% of simulations stays a fail.
- A method passes if all 8 rows pass. The horizons below the floor are listed
  per row as "conservative" and carried into every grade that uses the gate.
- New gate record: `{alpha: 0.05, ceiling: 0.075, floor_warning: 0.025,
  max_share_undefined: 0.05, rule: one_sided}`. A summary carrying the old
  two-sided gate no longer unlocks anything.

## 2. Why (operator)

- **Flattering is the harm.** A method that says "edge found" too often on
  no-edge data stores false findings, and later combinations build on them.
  That is never accepted.
- **Too strict only costs power.** A method below the floor misses some real
  effects but never invents one. That is a cost, reported as "conservative",
  not a reason to refuse every verdict.
- This is the usual meaning of a valid test: false-positive rate at most
  alpha. The two-sided band of amendment 3 was a symmetric choice, not a
  validity requirement.

## 3. Disclosed: what was known when this was decided

- **The gate results were known.** This rule was decided after the shuffle
  method's (B, `block_permutation_v1`) gate numbers were published
  (`REGRADE_run065.md`). Under the old rule B failed only the floor (lowest
  0.0225); its highest value was 0.0575. Under this rule B passes for
  Donchian(20). The change is chosen knowing that consequence.
- **No claim result was known.** No run_065 effect size, p-value or verdict
  has been computed or seen by anyone (REGRADE_run065.md, "NOT computed").
  The rule therefore cannot have been chosen to steer run_065's verdict.
- The other methods are not rescued: A (`a851a_episode_v1`) fails on "no
  answer" (100%), and amendment 4's `a851a_episode_timegap_v1` breaks the
  ceiling (up to 0.125). Both stay failed.

## 4. No re-run: the existing B cells are re-evaluated

- The gate itself is not re-run and not changed: same simulations, same 400
  per cell, same N = 199 fakes, same alpha. Only the pass rule is applied
  anew to the existing cell files in `calibration/cell_block_permutation_v1_*.yaml`.
- **Provenance.** Those cells were produced by the code committed in
  `bc4e67f4` and carry no per-cell code hash (they predate it). The
  re-evaluated summary records the sha256 of the two producing files read
  from `bc4e67f4` itself, and the sha256 of each cell file it read. The
  audit caveat of REGRADE_run065.md stands: that code and those results were
  committed together, so no commit proves the code was frozen first.
- **Method B code unchanged since.** Between `bc4e67f4` and this branch's
  base, `tools/claim_tests.py` changed only in the A8.5.1a family, the lock
  and the CLI; `fake_window`, the selectors, outcomes, baselines, statistics
  and the B branch of `run_test` are unchanged. The calibration script changed
  only in metadata, the period option and seeds for other periods; period-20
  seeds for B are the same.
- **Disclosed, unchanged:** the gate counted p < 0.05 with N = 199 (a valid
  method rejects at most 0.045); the grade uses N = 1,000 (at most 0.04995).
  The grade can reject slightly more often than the gate measured, by about
  0.005 at most for a valid method. B's highest value, 0.0575, leaves room
  under the 0.075 ceiling.

## 5. Per signal: only Donchian(20) has a B calibration

run_065 trades two signals:
- `DonchianBreakoutComponent(period=20)`: variants `base` (BTCUSD) and
  `donchian_solusdt_crossasset` (SOLUSD);
- `DonchianBreakoutComponent(period=14)`: variant `donchian_period_14_reactive`
  (BTCUSD).

B's gate was run on Donchian(20) only. **No B calibration exists for
Donchian(14)**, and running one would be a new gate run, which this slice
does not do (operator: no re-run). So `donchian_period_14_reactive` is **not
graded** (amendment 4 section 4): listed, its effect sizes reported as the
tool always does, no verdict, and it masks nothing.

## 6. The grade, exactly as fixed

For the variants trading Donchian(20), with method B as the spec's default
(`block_permutation_v1`, N = 1,000, seed 20261003), using the pre-registered
spec `run_065_breakout_continuation.yaml` unchanged:
- tests `upper_breakout` (forecast >= 12, direction greater) and
  `lower_breakout` (forecast <= -12, direction less), horizons 1-5 days,
  statistic mean difference against all other days;
- floor: 100 events and 4 windows at every horizon;
- window-sign rule: the right sign in at least 4 of 6 windows;
- **refuted** only when the wrong-way effect is itself significant
  (p_opposite < 0.05) at some horizon; **supported** only when right way with
  p < 0.05 at every horizon and the sign rule met; **inconclusive** otherwise;
- the claim is supported only if both tests are; across variants refuted
  dominates; N tests run = 2 tests x graded variants.

**Reading a B verdict with this gate:** B is conservative in some cells
(section 1), so an "inconclusive" is weaker evidence of "no effect" than it
would be under an exactly-sized test. A "supported" is not weakened.

## 7. Unchanged rules

- `claim_status` is information only: it never changes `idea_status`, never
  routes, never bans (D-055).
- The claim test runs only after a completed backtest, on saved bars.

## 8. Order of commits

1. This amendment.
2. The code that applies the one-sided rule, and its tests.
3. Review notes (Opus adversarial review of this amendment and the code).
4. The re-evaluated B summary.
5. The run_065 grade and the updated REGRADE_run065.md.
