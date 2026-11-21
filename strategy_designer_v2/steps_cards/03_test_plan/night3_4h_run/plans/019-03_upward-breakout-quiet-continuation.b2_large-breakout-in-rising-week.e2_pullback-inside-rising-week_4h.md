---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0974d5467d9f
---
Fidelity:
- Situation: the 4h close sits farther below the highest high of the preceding two days, measured in the 30-day average 4h range -> kept: BreakoutInMeanRangesComponent "below" computes max(0, H − close)/B, with H over the prior 12 bars (bar t excluded) and B over 180 bars.
- Comparison: the depth is judged only while the coin's 7-day return is positive -> kept: a regime rule turns the idea on when the 42-bar return is above 0, and every other bar is flat.
- Outcome: the coin rises more over the next three days, and the deeper the pullback the larger the rise -> kept: the horizon is 18 bars and the position is long, sized by the pullback's depth.
- Verdict transfer: yes: the config measures the same pullback depth, under the same condition, over the same horizon, so its result carries over to the idea.
Forecast: The regime is active only while the coin's 42-bar (7-day) return is above 0; on every other bar the forecast is 0. - Indicator: BreakoutInMeanRangesComponent with side "below", period 12 and base_period 180. It is how far the close sits below the highest high of the prior 12 bars, counted in the mean 4h bar range of the last 180 bars. - Scaling: it is standardised over its last 180 values (min_periods 45), so a typical pullback gives about +10, capped at +20. - Sign: it is 0 when the close is at or above the prior high and grows linearly with the depth of the pullback. It is never negative, so the forecast is long-only. - Combination: this one component is the whole forecast.
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Take each window's non-overlapping 18-bar grid, from its first row, and keep the grid bars with forecast > 0. On those bars, take the coin's 18-bar forward return minus its normal drift (its mean 18-bar return over all windows). Pool across coins and regress this excess return on the forecast; the measure is the slope's t.
- Supporting check: The mean of (forecast × excess return) over the same grid bars is above 0. This is the timing gain before costs, net of holding the coin.
- Confirm: The slope's t is 2 or more and the supporting check passes, with at least 100 cases.
- Reject: The slope's t is -2 or less, with at least 100 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t whose supporting check fails, and so is any result from fewer than 100 independent grid cases with forecast > 0.
