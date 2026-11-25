---
plan: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d
idea: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 20-bar excess return on forecast (positive-forecast grid bars): 0.0135211; OLS slope t: 2.72461 (threshold: slope t >= +2 with >= 100 cases to confirm (with top-minus-bottom third > 0); t <= -2 with >= 100 cases to reject)
- Supporting check: top-third minus bottom-third mean excess return: 0.223046, passed: True
- Counts: positive-forecast grid cases: 47
- Decided by: Fewer than 100 positive-forecast grid cases (47), so the minimum count is not reached.
- Reading: The coin's mean 20-bar return is taken over all its grid bars (positions 0, 20, 40, ... of each window) in all windows; thirds are the floor(n/3) lowest and highest forecasts after a stable sort; fewer than 100 cases is reported as not observable per the minimum-count rule.
- Size: unusual move +1.02 % (t 0.23, the cases of one day together: 35 days) per case over 20 bars, 0.017 of the coin's usual move (25.32 %); normal drift in its direction +0.55 %, total +1.57 %; 42 cases
Plan: `steps_cards/03_test_plan/validation_run/plans/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d.md`
Record: `steps_cards/04_backtest/validation_run/unseen_coins/backtests/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d`
Measure: `measure.py`
