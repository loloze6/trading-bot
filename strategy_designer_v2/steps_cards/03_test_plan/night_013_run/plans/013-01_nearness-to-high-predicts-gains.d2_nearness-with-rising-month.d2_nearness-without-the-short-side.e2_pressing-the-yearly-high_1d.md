---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's daily close sits near its highest close of the past 52 weeks -> kept: DistanceFromHigh over 364 daily closes, graded by how close the close is to that high.
- Comparison: nearer to the high versus farther below it -> kept: the forecast grows as the distance shrinks and is centred on the coin's usual distance.
- Outcome: a higher return over the next 7 days, concentrated in the closes nearest the high -> kept: the 7-bar forward return of the largest positions is compared with holding and with the next-closest bars.
- Verdict transfer: yes: the test measures closeness to the 52-week high and the 7-day return that follows, as the idea states them.
Forecast: DistanceFromHighComponent with period 364 (52 weeks of daily bars) gives the percent the close sits below its highest close. It is 0 at a new high and negative below it. It is standardised over its past 364 values, so it reads about -10 at the coin's usual distance, about 0 at the high, and down to -20 far below. A constant +10 offset with equal weight is added. The forecast is (x + 10) / 2. It is about +5 when the coin presses its 52-week high, 0 at its usual distance, and down to -5 when it sits twice its usual distance below the high. It is graded throughout and grows linearly with closeness to the high.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The sample is the non-overlapping 7-bar grid in each window (positions 0, 7, 14, ...). Take the bars in the top quintile of forecast, pooled over coins and windows; these are the closes nearest the 52-week high. For each, measure the 7-bar forward return minus the coin's mean 7-bar return over all its windows (holding). Report the mean of these excess returns and its t.
- Supporting check: The top quintile's mean 7-bar forward return exceeds the fourth quintile's (Welch t above 0). This checks that the gain is concentrated at the high, not merely in the upper part of the range.
- Confirm: The top-quintile mean excess return over holding has t ≥ 2, and the supporting check passes.
- Reject: The top-quintile mean excess return over holding has t ≤ -2.
- Inconclusive: A t between -2 and 2, or t ≥ 2 with the supporting check failing. At least 100 independent top-quintile cases are required; with fewer, the result is inconclusive.
