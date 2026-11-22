---
plan: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h
idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean short-side 48-bar unusual move per weekend case: 0.00323226; t of the weighted mean: 1.30238 (threshold: confirm: weighted mean > 0 with t >= 2 and supporting check passing; reject: weighted mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger half of |forecast| minus smaller half: 0.0024088, passed: True
- Counts: cases: 1032
- Decided by: t lies between -2 and 2.
- Reading: Situation bars are Sunday 23:00 UTC bars with a positive weekend 48-bar rise (component raw value, else price return) and last-48-bar mean volume below the prior 120 bars' mean (regime used when history is short); drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; the t is that of the |forecast|-weighted mean (weighted-residual standard error with n/(n-1) correction); the halves split all cases pooled by sorted |forecast| (smaller half gets the extra case when odd) with unweighted half means; fewer than 100 cases is treated as not observable.
- Size: unusual move +0.29 % per case over 48 bars, 0.045 of the coin's usual move (6.56 %); normal drift in its direction -0.27 %, total +0.03 %; 924 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h`
Measure: `measure.py`
