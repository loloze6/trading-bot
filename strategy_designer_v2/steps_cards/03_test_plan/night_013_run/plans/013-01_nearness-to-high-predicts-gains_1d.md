---
idea: 013-01_nearness-to-high-predicts-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: how close the daily close sits to its highest close of the past 52 weeks -> kept: percent distance from the 364-bar highest close, graded.
- Comparison: closer to the high versus farther below it, for the same coin -> kept: the distance is set against its own usual depth, so the forecast is long when the coin is closer than usual and short when it is farther.
- Outcome: higher return over the next 30 days the closer the coin is to the high -> kept: the 30-bar forward return, before costs, set against holding the coin.
- Verdict transfer: yes: the forecast grows with closeness to the 52-week high, so gains that grow with the forecast over 30 bars are the idea's own claim.
Forecast: Two components are averaged with equal weights. - `DistanceFromHighComponent` with `period` 364 (52 weeks of daily bars) measures how far the close sits below its 364-bar highest close. It is 0 at the high and more negative the deeper the fall. - It is standardised against its own past 364 values (`min_periods` 91), which puts it between about -20 (deep below the high) and 0 (at the high), with an average of about -10. - A constant +10 (`BuyAndHoldStrategy`, standardised) is added to centre it. The forecast is (x + 10) / 2, where x is the standardised distance: - about +5 at a new 52-week high; - 0 when the distance is at its usual depth; - negative, down to about -5, when the coin is farther below its high than usual. It is continuous and grows steadily with closeness. There is no regime: the rule applies on every bar.
Config: 013-01_nearness-to-high-predicts-gains_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The slope, pooled over all coins and windows, of each coin's 30-bar forward return on the forecast at bar t. The return is close[t+30]/close[t] - 1 minus that coin's mean 30-bar return over all windows. Samples are non-overlapping, at bars 0, 30, 60, 90 of each window, so no return crosses a window. The slope's t is reported with the number of cases.
- Supporting check: The book's timing gain is above zero. This is the book's mean daily return before costs minus its gain from the market's own rise.
- Confirm: The slope's t is 2 or more, and the timing gain is above zero.
- Reject: The slope's t is -2 or less, meaning a closer distance to the high is followed by lower returns than usual.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with a timing gain of zero or below is also inconclusive. At least 300 non-overlapping 30-bar cases are needed; with fewer, the result is inconclusive.
