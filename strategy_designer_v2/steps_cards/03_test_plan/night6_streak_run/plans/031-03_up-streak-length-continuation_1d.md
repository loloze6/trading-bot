---
idea: 031-03_up-streak-length-continuation
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8342b7be17d6
---
Fidelity:
- Situation: the coin has closed higher several days in a row -> kept: the current run of higher closes, n, is 0 when today did not close higher.
- Comparison: the run's length against the coin's own up-close streaks over the past 365 days -> kept: n is divided by the mean length of the completed up streaks in the last 365 bars.
- Outcome: the coin keeps rising over the next 5 days, more after a longer streak -> kept: the long position grows with the relative streak length and is held 5 bars.
- Verdict transfer: yes: the forecast is the idea's own measure, so a confirm or reject here answers the idea directly.
Forecast: The forecast uses `UpCloseStreakLengthComponent` with side "up", base "mean_streak", base_window 365 and max_bars 30. Its value is the current run of higher closes divided by the mean length of the coin's completed up streaks over the past 365 days. It is standardised against its own past 366 values. The forecast is 0 on any day that did not close higher, so the book is flat there. It is positive during an up streak and grows in proportion to how long the streak is against the coin's usual streak. It is never negative.
Config: 031-03_up-streak-length-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return on the forecast. The return is taken in excess of the coin's mean 5-bar return over all windows, which is the holding-the-coin baseline. The sample is the non-overlapping 5-bar grid of every window and coin, using bars with a recorded forecast. The t-statistic is computed with the cases of one day taken together.
- Supporting check: On grid bars in the top third of positive forecasts, the mean excess 5-bar return must be above the mean on grid bars with forecast 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes.
- Reject: The slope is negative with t ≤ -2, meaning longer streaks are followed by weaker 5-day returns than usual.
- Inconclusive: Any slope with |t| < 2 is inconclusive, as is a positive slope with t ≥ 2 when the supporting check fails. The test needs at least 200 grid bars with a positive forecast, spread over at least 150 distinct days; with fewer, the result is inconclusive.
