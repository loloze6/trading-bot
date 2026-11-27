---
plan: 077-01_choppy-agitated-wide-low-close-rebound_1d
idea: 077-01_choppy-agitated-wide-low-close-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return on case bars (forecast > 0): 0.0083275; t of the mean, cases clustered by day: 1.95992 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess return on forecast size: -5.25389e-05, passed: False
- Counts: case bars: 213, distinct case days: 164
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is checked on its core conditions (range / mean of the last 30 bar ranges, current bar included, at least 1.0; (close - low)/(high - low) at most 0.25; forecast positive) over active bars with 30 bars of in-window history, the code-added profile vetoes being only removals and not rebuildable from in-window bars; cases are all bars with forecast > 0 (every bar, horizon 1), the day-clustered t sums deviations per UTC day with a G/(G-1) correction, and the plan's 30-distinct-case-day minimum is treated as a minimum count (not observable).
- Size: unusual move +0.84 % (t 1.94, the cases of one day together: 161 days) per case over 1 bars, 0.162 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.98 %; 204 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-01_choppy-agitated-wide-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-01_choppy-agitated-wide-low-close-rebound_1d`
Measure: `measure.py`
