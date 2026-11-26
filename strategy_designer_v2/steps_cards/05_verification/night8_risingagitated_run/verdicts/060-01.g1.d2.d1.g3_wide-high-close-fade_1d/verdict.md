---
plan: 060-01.g1.d2.d1.g3_wide-high-close-fade_1d
idea: 060-01.g1.d2.d1.g3_wide-high-close-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: size-weighted mean next-day short excess gain: 0.00617508; t of the weighted mean, cases grouped by day: 2.3639 (threshold: t >= 2 confirms (with supporting check < 0); t <= -2 rejects)
- Supporting check: wider-range half minus narrower half, mean next-day excess return: -0.00622419, passed: True
- Counts: distinct days with a case: 669, cases: 1380
- Decided by: The main measure's t is 2 or more and the supporting check is below 0.
- Reading: Situation = close location (close-low)/(high-low) > 0.5 recomputed from prices, with the falling-agitated profile read from the recorded regime (its 365-bar volatility lookback cannot be rebuilt inside a window), side short; t of the size-weighted mean groups size-weighted deviations per UTC day; the wider half is |forecast| strictly above the median, the narrower half the rest, compared on next-day return minus the coin's all-window mean; fewer than 30 days gives 'not observable'.
- Size: unusual move +0.55 % (t 2.13, the cases of one day together: 501 days) per case over 1 bars, 0.113 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.42 %; 954 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003332 on the check folds against +0.006175 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1.g3_wide-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2.d1.g3_wide-high-close-fade_1d`
Measure: `measure.py`
