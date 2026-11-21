---
plan: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-bar drift-adjusted forward return on mom28 forecast, trending grid bars: 0.00111455; OLS t of slope: 3.97145 (threshold: confirm: slope > 0 with t >= 2 (and supporting check > 0); reject: slope < 0 with t <= -2)
- Supporting check: book mean daily return minus market-rise gain, before costs: 0.000750084, passed: True
- Counts: grid cases on trending bars: 1766, book days: 2898
- Decided by: The slope is positive with t >= 2, and the book's mean daily return minus its gain from the market's rise is above 0.
- Reading: Before costs, the book's daily return is the position held after the previous bar times the coin's close-to-close return, averaged over coins per day; the drift is the mean of each coin's non-overlapping 5-bar grid returns over all its windows; the fewer-than-200-cases rule is applied as a minimum count (not observable).
- Size: unusual move +0.86 % per case over 5 bars, 0.078 of the coin's usual move (10.60 %); normal drift in its direction +0.10 %, total +0.96 %; 1404 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d`
Measure: `measure.py`
