---
plan: 048-05_falling-agitated-up-week-reversal_1d
idea: 048-05_falling-agitated-up-week-reversal
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of y (3-day return minus coin mean) on |forecast|, grid bars with forecast < 0: -0.927907; OLS slope t: -0.927907 (threshold: confirm: t <= -2 and mean y < 0; reject: t >= +2 and mean y > 0; fewer than 50 cases: not decidable)
- Supporting check: mean y below 0: -0.00451418, passed: True
- Counts: active bars: 908, cases (grid bars with forecast < 0): 301
- Decided by: With at least 50 cases, the slope's t and the mean y meet neither the confirm nor the reject rule. No effect (common/verdicts.md): t in the idea's direction +0.928 (below 1), 301 cases (30 needed).
- Reading: Profile on each bar is read from the recorded regime (the 365-bar volatility percentile cannot be rebuilt inside a window) plus the 7-day return > 0 and the 60-day percent move < -10 where computable; the coin's mean 3-day return is the mean over the same non-overlapping grid of all its windows; fewer than 50 cases is reported as not observable.
- Size: unusual move +0.12 % (t 0.21, the cases of one day together: 187 days) per case over 3 bars, 0.008 of the coin's usual move (8.38 %); normal drift in its direction -0.19 %, total -0.07 %; 303 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.928 (below 1), 301 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/048-05_falling-agitated-up-week-reversal_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/048-05_falling-agitated-up-week-reversal_1d`
Measure: `measure.py`
