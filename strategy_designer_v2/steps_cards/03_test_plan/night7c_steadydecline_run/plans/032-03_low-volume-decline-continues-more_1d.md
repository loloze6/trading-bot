---
idea: 032-03_low-volume-decline-continues-more
brief: 032_calm-decline-keeps-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: a coin that has fallen over the past 28 days -> kept: a regime where the 28-day return is below 0, flat outside it.
- Comparison: volume over those 28 days against the coin's own usual volume -> adapted: the log ratio of the 28-day mean volume to the prior year's mean, graded so the short grows as the ratio falls below 1.
- Outcome: a further fall over the next 5 days, larger the lower the volume -> kept: a short held 5 bars, larger when volume is thinner.
- Verdict transfer: yes: the test grades short size by the idea's volume ratio, only inside 28-day declines, over the idea's 5-day horizon.
Forecast: The regime is the 28-day decline. On each bar, `PriceEvolutionOnPeriodComponent` (28) measures the 28-day return, and a bar with a return below 0 is `trending`. Every other bar is flat. Inside a decline, `VolumeRatioComponent` gives ln(r). Here r is the mean volume of the last 28 bars over the mean volume of the 365 bars before them, so the two windows do not overlap. `standardise` puts ln(r) on the forecast scale (window 393, min_periods 98). A `clip` at max 0 keeps only the short side. The forecast is 0 when the 28-day volume is at or above the usual volume. It is negative when volume is below usual, and the short grows continuously as volume thins, up to -20.
Config: 032-03_low-volume-decline-continues-more_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the regime (`trending`) bars at the non-overlapping 5-bar grid positions of each window. Regress each coin's 5-bar forward return, minus that coin's mean 5-bar return over all windows, on the recorded forecast. Take the slope and its t; the cases of one day are taken together.
- Supporting check: Over the grid cells with forecast ≤ -2, the mean excess 5-bar return in the short direction (the negated excess return) must be above 0.
- Confirm: The slope is positive with t ≥ 2: a more negative forecast (thinner volume) is followed by a larger fall than the coin's drift. The supporting check must also pass.
- Reject: The slope is negative with t ≤ -2: thinner-volume declines fall less than heavy-volume ones.
- Inconclusive: Any slope with |t| < 2 is inconclusive. So is a slope with t ≥ 2 when the supporting check fails. At least 100 regime grid cells and 30 grid cells with forecast ≤ -2 are needed; with fewer, the result is inconclusive.
