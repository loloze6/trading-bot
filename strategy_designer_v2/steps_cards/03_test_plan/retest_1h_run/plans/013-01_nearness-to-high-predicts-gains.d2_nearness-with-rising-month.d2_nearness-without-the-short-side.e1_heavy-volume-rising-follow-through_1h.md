---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's daily volume relative to its own 20-day average volume, while its 30-day return is positive -> kept: the regime is the sign of the 720-bar return, and the measure is the mean of the last 24 bars' volume over the mean of the last 480.
- Comparison: the higher the relative volume, the higher the return; thin volume means refusing the trade -> kept: the position grows with the volume ratio above 1 and is flat at or below 1.
- Outcome: a higher return over the next 3 days -> kept: the 72-bar forward return.
- Verdict transfer: yes: the test measures the stated condition, the stated volume ratio and the stated 3-day return, with nothing replaced.
Forecast: Only on bars where the coin's 720-bar (30-day) return is above 0, the trending regime. On all other bars the forecast is flat. The indicator is VolumeRatioComponent, form "centred": the mean volume of the last 24 bars over the mean of the last 480 bars, minus 1. It is above 0 when the last day traded more than the 20-day average. It is standardised over 480 past values and clipped at 0. The forecast is therefore 0 when volume is at or below its average, so a thin-volume rise is refused. It is positive and grows smoothly as the day's volume rises further above its 20-day average, up to the +20 cap. It is never short.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Take the trending-regime bars on a non-overlapping 72-bar grid in each window. Regress each bar's 72-bar forward return, minus the coin's mean 72-bar return over all windows, on that bar's forecast. Pool all coins and report the slope's t.
- Supporting check: The mean excess 72-bar return of grid cases in the top third of positive forecasts, minus that of grid cases with forecast 0, must be above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2. Also inconclusive: a t of 2 or more while the supporting check fails. The test needs at least 100 pooled trending-regime grid cases, of which at least 30 have a positive forecast; with fewer it is inconclusive.
