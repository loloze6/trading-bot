---
idea: 013-05_longer-stall-bigger-breakout
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a coin closes above its prior 52-week high -> adapted: "after the break" made "while the close is above the prior 365-day closing high" (regime rule).
- Comparison: more days of the past 60 spent closing just under that high -> kept: StallUnderHighCountComponent (window 60, period 365, band 10 percent) grades the position.
- Outcome: larger return over the next 30 days -> adapted: 30-day holding dropped; position held only while above the high, outcome measured as the 30-bar forward return.
- Verdict transfer: yes: the forward 30-bar return on regime bars, set against the stall count, tests the idea's own claim in both directions.
Forecast: The forecast is active only on bars where the close sits above the highest of the prior 365 closes; on all other bars it is 0. On an active bar it is long and equals the stall count, scaled by `standardise`. The stall count is the number of the last 60 bars that closed below the prior 365-bar closing high and within 10 percent of it. It is 0 when there was no stall, so there is no position, and the long position grows with the number of stall days. It never goes negative.
Config: 013-05_longer-stall-bigger-breakout_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The sample is the bars of a non-overlapping 30-bar grid in each window (positions 0, 30, 60, ...) whose regime is trending. On those bars, take the coin's 30-bar forward return minus that coin's mean 30-bar return over all windows (the same grid). Regress this excess return on `stall.post_pipeline_value` across all coins, and read the slope's t-statistic.
- Supporting check: none
- Confirm: The slope is positive with t >= 2, on at least 30 cases.
- Reject: The slope is negative with t <= -2, on at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is any result on fewer than 30 trending grid bars.
