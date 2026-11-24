---
plan: 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d
idea: 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-bar excess return on forecast (before costs): 0.000405532; OLS t of the slope: 5.13284 (threshold: slope > 0 with OLS t >= 2 (and timing > 0) confirms; slope < 0 with t <= -2 rejects; |t| < 2 inconclusive)
- Supporting check: timing part of the book's mean daily return (mean minus market-rise gain): 0.000752334, passed: True
- Counts: bars with a non-zero forecast: 2918, bars in the slope: 2897
- Decided by: The slope is positive with t >= 2 and the timing part of the book's mean daily return is above 0.
- Reading: The slope is an OLS of next-bar excess return on forecast with an intercept over every recorded bar with a next close in its window (forecast-0 bars included), XMR's mean daily return is the pooled close-to-close mean of all windows, the book's daily return is postRebalance_total_value bar to bar inside each window with the market part being the prior bar's allocation times that mean, and the minimum of 500 non-zero-forecast bars is counted over all recorded bars and, if missed, gives 'not observable'.
- Size: unusual move +0.48 % (t 4.57, the cases of one day together: 1896 days) per case over 1 bars, 0.104 of the coin's usual move (4.65 %); normal drift in its direction -0.00 %, total +0.48 %; 1896 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d`
Measure: `measure.py`
