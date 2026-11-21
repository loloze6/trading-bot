---
plan: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess return on forecast: 0.000470152; OLS slope t: 1.0924 (threshold: slope t >= +2 with >= 200 cases and timing gain > 0 confirms; slope t <= -2 with >= 200 cases rejects)
- Supporting check: timing gain (book mean daily return before costs minus market-rise gain): 0.000773056, passed: True
- Counts: cases: 1691
- Decided by: slope t lies between -2 and +2
- Reading: all grid cases are kept, including those with a zero forecast, in a pooled OLS with intercept on the coin's drift-removed 10-bar return; the book's return before costs is the held position times the next bar's coin return, averaged over coins per day.
- Size: unusual move +1.37 % per case over 10 bars, 0.083 of the coin's usual move (14.49 %); normal drift in its direction +0.34 %, total +1.71 %; 986 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d`
Measure: `measure.py`
