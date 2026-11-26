---
plan: 031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d
idea: 031-02.b1.b2.b2_sharp-rebound-near-low-fails
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 20-bar forward return (net of coin drift) on 60-bar return, mean_reversion grid bars, all coins pooled: -0.0234782; slope t, day-clustered: -0.640598 (threshold: confirm: slope < 0 with t <= -2 and supporting check > 0; reject: slope > 0 with t >= +2; else inconclusive)
- Supporting check: mean unusual move of short cases, signal direction, net of drift: -0.0257756, passed: False
- Counts: grid cases inside the regime: 417, distinct days: 65, short cases (supporting check): 276
- Decided by: The slope's |t| is below 2 (or cannot be computed): inconclusive.
- Reading: Cases are the mean_reversion bars at window positions 0,20,40,... with a 20-bar forward return inside the window; the 60-bar return is recomputed from closes inside the window only, so grid bars with fewer than 60 prior bars in their window are left out; drift is each coin's mean 20-bar return over its grid in all windows; the slope's t uses day-clustered standard errors; the supporting check uses the grid cases inside the regime with a short forecast; minimum counts are on the regression cases.
- Size: unusual move -1.07 % (t -0.46, the cases of one day together: 271 days) per case over 20 bars, -0.002 of the coin's usual move (24.73 %); normal drift in its direction -3.44 %, total -4.51 %; 449 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d`
Measure: `measure.py`
