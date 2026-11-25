---
plan: 059-01.b1_choppy-calm-rise-more-coins_1d
idea: 059-01.b1_choppy-calm-rise-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 7-day return (coin mean 7-day return removed): 0.0120015; t of the weighted mean, cases of one day summed: 0.990161 (threshold: confirm: > 0 with t >= 2 and slope > 0; reject: < 0 with t <= -2)
- Supporting check: OLS slope of excess 7-day return on forecast: 0.00233574, passed: True
- Counts: distinct days with cases: 163, cases: 409
- Decided by: the t of the main measure is between -2 and 2 (inconclusive rule)
- Reading: cases are grid bars (positions 0, 7, 14, ... of each window) with forecast > 0 and a 7-bar forward return inside the window; the t is the weighted mean over its day-clustered standard error (per day the sum of weight x deviation, with D/(D-1) correction); the plan's minimum of 30 distinct days is applied as 'not observable' as the workflow requires.
- Size: unusual move +0.30 % (t 0.52, the cases of one day together: 490 days) per case over 7 bars, 0.015 of the coin's usual move (12.84 %); normal drift in its direction +0.97 %, total +1.26 %; 803 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1_choppy-calm-rise-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1_choppy-calm-rise-more-coins_1d`
Measure: `measure.py`
