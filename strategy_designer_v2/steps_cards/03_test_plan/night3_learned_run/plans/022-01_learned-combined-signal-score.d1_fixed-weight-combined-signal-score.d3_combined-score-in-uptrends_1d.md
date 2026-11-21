---
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the four signals combined into one score, each weighted by its past predictive power -> kept
- Comparison: only while the coin's 28-day return is up, against the bars where it is not -> kept
- Outcome: the 5-day return is higher, and the rise larger, the higher the score -> kept
- Verdict transfer: yes: the composite, its gate and its 5-day horizon are built as the idea states them, so a confirm or a reject carries over to the idea.
Forecast: A regime rule reads the 28-day price change at each daily close. While that change is above zero, the bar is "trending". On every other bar the forecast is 0 (flat), because the idea holds only while the month is up. On trending bars the forecast is the past-predictive-power composite of four signals, all at the brief's conventions: 28-day momentum, 1-day reversal, nearness to the 90-day high, and negative 30-day volatility. Each signal is z-scored over 365 days and weighted by its correlation with the next 5-day return over the past 365 days, relearned on every bar. The composite is standardised over 365 past values with 91 minimum periods. The forecast is long when the score is positive and short when it is negative, and it grows continuously with the score.
Config: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the grid bars at positions 0, 5, 10, … of each window, using only bars whose regime is "trending" and whose forecast is not zero. On those bars, regress the coin's 5-bar forward return minus the coin's normal 5-bar drift on the forecast. The drift is the coin's mean over all windows. The measure is the t of the slope, with the count of cases given beside it.
- Supporting check: The book's mean daily return minus its gain from the market's own rise (the timing part) must be above 0.
- Confirm: The slope's t is 2 or more, with at least 200 cases, and the timing part of the book is positive.
- Reject: The slope's t is -2 or less, with at least 200 cases.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a timing part of 0 or below, is inconclusive. Fewer than 200 non-overlapping trending cases across all coins and windows is also inconclusive.
