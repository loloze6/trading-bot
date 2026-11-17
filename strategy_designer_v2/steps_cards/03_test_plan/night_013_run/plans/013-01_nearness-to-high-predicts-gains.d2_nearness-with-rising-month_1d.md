---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the close sits near its highest close of the past 52 weeks, while the 30-day return is positive -> kept
- Comparison: closer to the high against farther below it, and a higher 30-day return against a lower one -> kept
- Outcome: a higher return over the next 7 days, upward -> kept
- Verdict transfer: yes: the gate, the nearness, the 30-day return and the 7-day horizon are each measured as stated.
Forecast: A regime rule makes the forecast active only while the 30-day price change, PriceEvolutionComponent(30), is above 0. On every other bar the forecast is 0. Inside that regime the forecast is the equal-weight mean of two standardised components: - Nearness to the high. DistanceFromHighComponent(364) is 0 at a 52-week closing high and more negative the deeper the close sits below it. It is standardised over 364 bars, so it adds nothing at the high and pulls the forecast down the farther price sits below the high. - The 30-day return. PriceEvolutionComponent(30) is standardised over 60 bars. It is positive throughout the regime and grows as the month's rise grows. The forecast is therefore largest when the coin is at its high after a strong month. It shrinks towards 0 with distance from the high or with a weaker month. It can turn slightly negative only when the coin is far below its high after a small rise. No offset forces it to stay long, because a constant inside a regime is not allowed.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The cases are the bars on a non-overlapping 7-bar grid in each window, on which the regime is `trending`. For each case, take the coin's 7-bar forward return minus the coin's mean 7-bar return over all windows. Regress that excess return on the bar's forecast and read the slope's t.
- Supporting check: Split the book's mean daily return before costs into the gain from the market's own rise and the rest, which is timing. The timing part must be above 0.
- Confirm: The slope is above 0 with t ≥ 2, and the timing gain is positive.
- Reject: The slope is below 0 with t ≤ -2.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive. A slope with t ≥ 2 but a timing gain of 0 or less is also inconclusive. At least 100 non-overlapping in-regime cases are required across coins and windows; with fewer, no verdict is given.
