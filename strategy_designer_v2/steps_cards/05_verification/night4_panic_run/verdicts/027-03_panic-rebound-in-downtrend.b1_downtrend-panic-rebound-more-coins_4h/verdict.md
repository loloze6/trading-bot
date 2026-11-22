---
plan: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h
idea: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 84-bar return of bets over the coin's mean 84-bar return: -0.023502; t of the mean: -5.28546 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and top-minus-bottom third > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: top-third minus bottom-third excess return by entry forecast: 0.00183887, passed: True
- Counts: cases: 1724, active_bars: 75645, top_third_cases: 574, bottom_third_cases: 574
- Decided by: Mean excess return below 0 with t <= -2 over at least 30 cases.
- Reading: Situation = 180-bar close return ending 6 bars ago below 0 (recomputed from prices inside each window, active bars in a window's first 186 bars left out of the agreement as not computable) and close below the prior 24h high (raw component > 0), side long; a case is the first long bet (forecast rise >= 2 from its lowest positive level since the last bet, reset at flat) in each 84-bar grid cell from each window's first row; the coin's mean 84-bar return uses the same non-overlapping grid over all its windows; terciles are the n//3 highest and n//3 lowest forecasts at entry after a stable sort.
- Size: unusual move -2.35 % per case over 84 bars, -0.093 of the coin's usual move (22.11 %); normal drift in its direction +2.80 %, total +0.45 %; 1724 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h`
Measure: `measure.py`
