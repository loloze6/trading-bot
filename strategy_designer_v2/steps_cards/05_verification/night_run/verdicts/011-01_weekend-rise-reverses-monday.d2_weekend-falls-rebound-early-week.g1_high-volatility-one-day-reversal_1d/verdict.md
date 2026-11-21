---
plan: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean market-adjusted position gain per bar, 1 bar, pooled: 0.000852862; ordinary t of the mean: 3.99628 (threshold: confirm t >= 2 with supporting check > 0; reject t <= -2; otherwise inconclusive; >= 1000 non-zero-position bars)
- Supporting check: top third minus bottom third of |forecast|, sign(forecast) x (next-day return - coin mean): 0.00321289, passed: True
- Counts: bars with a non-zero position: 17312, bars in main measure: 17380
- Decided by: The mean market-adjusted gain has t >= 2 and the top-minus-bottom third difference is greater than 0.
- Reading: The plan's situation (a large move faded) is read as any non-zero 1-bar move with the forecast on the opposite side, taken from the in-window price return (the component's raw value on a window's first bar); the main measure is pooled over every bar with a next-bar return (zero positions included, as 'on every bar' says), the thirds are split by rank of |forecast| over all such bars (bottom n//3 and top n//3), and the 1000-bar minimum counts bars with a non-zero position that have a next-bar return.
- Size: unusual move +0.22 % per case over 1 bars, 0.047 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.22 %; 9287 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d`
Measure: `measure.py`
