---
plan: 049-01_choppy-scaled-five-day-rise-continuation_1d
idea: 049-01_choppy-scaled-five-day-rise-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar forward return on cases (forecast > 0, non-overlapping 3-bar grid): -0.000851589; t of the mean, cases of a day pooled: -0.288967 (threshold: confirm: mean > 0 with day-pooled t >= 2 and top-minus-bottom > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess of top-half forecast cases minus bottom half: -0.00215057, passed: False
- Counts: cases: 717, distinct days: 392
- Decided by: Main t between -2 and 2 (inconclusive rule).
- Reading: Choppy profile taken as the bars whose regime is 'unknown' (neither 60-bar trend veto fired), the 5-day rise as raw scaled_rise > 0 (price 5-day return where missing); top half = cases with forecast above the cases' median, bottom half = at or below it; the day-pooled t sums the cases' deviations from the mean per UTC day; the plan's 'fewer than 100 cases or 60 days' is applied as 'not observable'.
- Size: unusual move -0.27 % (t -1.07, the cases of one day together: 580 days) per case over 3 bars, -0.037 of the coin's usual move (7.96 %); normal drift in its direction +0.35 %, total +0.07 %; 859 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/049-01_choppy-scaled-five-day-rise-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/049-01_choppy-scaled-five-day-rise-continuation_1d`
Measure: `measure.py`
