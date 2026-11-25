---
idea: 037-02_falling-market-range-jump-decline
brief: 037_wide-days-precede-decline-in-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: f9d41455da54
---
Fidelity:
- Situation: in a falling market, a day whose high-low range is wide against the coin's 30-day average daily range -> adapted: "wide" becomes a regime condition, the day's range at or above 1.5 times its 30-day mean range (the usual wide-range-bar convention); inside it the position is graded by that ratio, and code adds the falling profile.
- Comparison: wider days against narrower ones, and the decline against holding the coin -> kept: the position grows with the range multiple, and returns are measured against the coin's drift.
- Outcome: decline over the next 3 days, larger after wider days -> kept: short for 3 bars from the wide day's close; "after" is made "while", and the 3-bar hold covers the 3 days.
- Verdict transfer: yes: the test shorts exactly the wide days in falling markets for 3 days, sized by range multiple, so its result is the idea's result.
Forecast: The raw value is the day's high-low range divided by the mean high-low range of the last 30 days, the current day included (RangeCompressionRatioComponent, short_period 1, long_period 30, base "mean_bar_range", form "width"). The regime detector selects "trending" only on days where this ratio is 1.5 or more; every other day is flat. Inside that regime, the same ratio is standardised over its past 60 values and negated. This gives a short whose size grows with the range multiple: a 1.5x day is about -15 and a 2x day reaches the cap of -20. The forecast is never positive. Code adds the falling-market profile, and the 3-bar hold keeps each short for the 3 days that follow.
Config: 037-02_falling-market-range-jump-decline_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move per case, in the short direction. A case is a bet: the forecast falls by at least 2 points on the short side, read once per 3-bar grid cell. For each case, take the coin's 3-bar return from the signal bar's close and subtract the coin's normal 3-bar drift, measured over all windows. Report the mean over the cases, with a t computed with each day's cases taken together.
- Supporting check: Across the cases, regress the 3-bar excess return on the raw range multiple (`last_history_value` of range_mult). The slope must be below 0: wider days are followed by deeper declines.
- Confirm: The mean unusual move in the short direction is positive with t ≥ 2, over at least 30 cases, and the supporting slope is negative.
- Reject: The mean unusual move in the short direction is negative with t ≤ -2: wide days in falling markets are followed by rebounds against the drift.
- Inconclusive: Any t between -2 and 2, a confirming main measure with a slope of 0 or above, or fewer than 30 cases (non-overlapping 3-bar cells).
