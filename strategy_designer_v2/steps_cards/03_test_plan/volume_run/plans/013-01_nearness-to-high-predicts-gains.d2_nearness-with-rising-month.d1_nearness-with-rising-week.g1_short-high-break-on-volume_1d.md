---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: daily close near its 20-day highest close, with that day's volume heavy against its 30-day average -> kept
- Comparison: closer to the high and heavier volume versus farther and thinner, as a graded relation -> kept
- Outcome: the coin's return over the next 7 days is higher -> kept
- Verdict transfer: yes: the forecast grows with closeness and with volume exactly as stated, and it is judged on 7-day returns against the coin's own average.
Forecast: The forecast is the equal-weight mean of two standardised parts. Each part is divided by the mean absolute value of its own previous 60 values and multiplied by 10, capped at ±20. - Closeness: DistanceFromHighComponent(period 20) is the percent below the highest close of the last 20 days. It is 0 at the high and more negative the deeper the close sits below it. - Volume: VolumeRatioComponent(period 30) is today's volume over its 30-day mean. It is about +10 on a day of average volume and larger on heavier days. The forecast is (closeness + volume) / 2. It is positive and grows when the close presses its 20-day high on heavy volume. It is negative when the close sits deep below the high on thin volume, and near 0 when the two parts balance. It is signed, continuous and ungated.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use non-overlapping 7-bar samples (positions 0, 7, 14, ... of each window), pooled over coins and windows. Regress the 7-day forward return minus the coin's mean 7-day return over all windows on the recorded forecast at t. Report the slope's t-statistic.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise, is above 0 (timing gain positive).
- Confirm: The slope t is 2 or more AND the timing gain is above 0.
- Reject: The slope t is -2 or less.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more with a timing gain at or below 0. At least 300 non-overlapping samples are required; with fewer the result is inconclusive.
