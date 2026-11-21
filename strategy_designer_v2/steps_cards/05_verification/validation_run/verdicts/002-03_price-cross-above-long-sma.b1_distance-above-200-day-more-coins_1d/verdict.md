---
plan: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d
idea: 002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 20-bar excess return on forecast (positive-forecast grid bars): 0.00404012; OLS slope t: 2.39877 (threshold: slope t >= +2 with >= 100 cases to confirm (with top-minus-bottom third > 0); t <= -2 with >= 100 cases to reject)
- Supporting check: top-third minus bottom-third mean excess return: 0.0502549, passed: True
- Counts: positive-forecast grid cases: 713
- Decided by: Slope t is at least +2 with at least 100 cases and the top-minus-bottom-third difference is above 0.
- Reading: The coin's mean 20-bar return is taken over all its grid bars (positions 0, 20, 40, ... of each window) in all windows; thirds are the floor(n/3) lowest and highest forecasts after a stable sort; fewer than 100 cases is reported as not observable per the minimum-count rule.
- Size: unusual move +2.16 % per case over 20 bars, 0.080 of the coin's usual move (22.86 %); normal drift in its direction +2.86 %, total +5.03 %; 641 cases
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b1_distance-above-200-day-more-coins_1d`
Measure: `measure.py`
