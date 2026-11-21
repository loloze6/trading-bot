---
plan: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
idea: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean of drift-adjusted 40-bar return / usual 40-bar move: 0.248673; t of the forecast-weighted mean: 2.03768 (threshold: confirm: > 0 with t >= 2; reject: t <= -2)
- Supporting check: calm minus violent half (median forecast split), mean drift-adjusted 40-bar return: -0.168923, passed: False
- Counts: cases: 122, high-forecast half: 61, low-forecast half: 61
- Decided by: The weighted mean meets the confirm rule but the calm-minus-violent difference does not reach > 0 with Welch t >= 2, so the result is inconclusive.
- Reading: Situation agreement is measured on the active bars where the cloud and the last outside side can be recomputed from the window's own prices (falling back to regime 'trending' with a long forecast only if none can); cases are long bets (forecast rise of >= 2 points from its low on the long side) read once per 40-bar grid cell from each window's first row with close[t+40] in the window; drift and usual move are the mean and std of each coin's non-overlapping 40-bar returns over all its windows; the weighted mean's t uses the forecast-weighted variance with effective n = (sum w)^2 / sum w^2; the median split drops cases equal to the median and compares unscaled drift-adjusted returns.
- Size: unusual move +11.07 % per case over 40 bars, 0.260 of the coin's usual move (30.89 %); normal drift in its direction +5.25 %, total +16.33 %; 122 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d`
Measure: `measure.py`
