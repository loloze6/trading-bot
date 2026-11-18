---
idea: 013-04_heavy-volume-below-high-breakout
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a coin closes above its prior 52-week high -> kept: regime on the close above the highest high of the prior 365 bars.
- Comparison: volume over the preceding 10 days against its own 90-day average -> kept: 10-bar mean volume over the 90-bar mean volume (the 10 bars end at the break bar).
- Outcome: larger return over the next 30 days with heavier volume, long -> adapted: holding period dropped; the position is held while the close stays above the prior high, and the 30-bar return is measured from the record's prices.
- Verdict transfer: yes: the test asks whether the 30-day return after a close above the prior 52-week high grows with the 10-to-90-day volume ratio, which is the idea's claim.
Forecast: A regime rule fires when the close is above the highest high of the prior 365 bars. The current bar is excluded from that high, so the distance is above 0 only on a break. On those bars the forecast is long and sized by the volume ratio: mean volume of the last 10 bars over mean volume of the last 90 bars. The ratio is standardised against its own past 90 values, so a ratio at its usual size gives about +10, a heavier one up to +20 and a lighter one less. It is always positive inside the regime. On every other bar the forecast is 0 (flat).
Config: 013-04_heavy-volume-below-high-breakout_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: Cases are break bars: a trending bar whose previous bar was not trending, with t+30 inside the same window, keeping only cases at least 30 bars after the previous kept case in that window. For each case, take the excess return: close[t+30]/close[t] - 1 minus the coin's mean 30-bar return over all windows. The measure is the OLS slope of excess return on the case's forecast (post_pipeline_value of vol_ratio), with its t-statistic, pooled over coins.
- Supporting check: none
- Confirm: The slope is positive with t >= 2, on at least 20 cases.
- Reject: The slope is negative with t <= -2, on at least 20 cases.
- Inconclusive: Any t between -2 and 2, or fewer than 20 independent cases, is neither a confirm nor a reject.
