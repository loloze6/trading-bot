---
idea: N5-03_high-in-confirmed-uptrend
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds B, C
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a close at or very near its 20-day high, while above the 200-day average with a positive 60-day return -> adapted: "near the 20-day high" becomes a graded range position with a strong dead zone; "above the 200-day average" and "positive 60-day return" stay on/off as the regime, because they are the idea's condition.
- Comparison: the rise is larger than the coin's usual 10-day move -> kept: the gain is judged against the coin's mean 10-day return over all windows.
- Outcome: a 10-day rise follows -> kept: the forward 10-bar return after the forecast is measured; the position follows the forecast and has no fixed holding period.
- Verdict transfer: yes: a strong range-top reading inside the two trend conditions is the idea's situation, and the 10-bar excess return is its outcome.
Forecast: The regime detector uses two settings. The close's percent distance from its 200-bar SMA must be above 0. The 60-bar price change must be above 0. When both hold, the bar is "trending"; on every other bar the forecast is flat. In "trending" the forecast is built from the 20-bar Donchian range position, in these steps: 1. The range position runs from -20 at the range low to +20 at the range high. 2. It is standardised over the past 60 values, with min_periods 20. 3. It is clipped at 0, so the forecast is long only. 4. It is raised by signed_power with exponent 3 and pivot 10, then clipped at 20. The forecast is 0 when the close is in the lower half of its 20-day range. It is close to 0 in the middle of the range: a standardised 5 becomes 1.25. It grows steeply as the close nears the 20-day high: 10 stays 10, and about 13 or more reaches the cap of 20. It is never negative.
Config: N5-03_high-in-confirmed-uptrend_1d_oos2_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take the bars where the forecast is 10 or more, pooled over all coins and windows. Measure the mean forward 10-bar close-to-close return on those bars, before costs. Subtract the coin's mean 10-bar return over all its test windows together. The t-statistic counts overlapping 10-bar returns once, using non-overlapping samples or a HAC estimate with lag 9.
- Supporting check: Rank correlation, across all trending bars, between the forecast and the forward 10-bar excess return. It should be positive.
- Confirm: The mean excess 10-bar return after forecasts of 10 or more is above 0 with t ≥ 2. There must be at least 30 non-overlapping cases.
- Reject: The mean excess 10-bar return after forecasts of 10 or more is below 0 with t ≤ -2. There must be at least 30 non-overlapping cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any result with fewer than 30 non-overlapping cases with forecast ≥ 10, whatever the estimate's sign.
