---
idea: 040-02_falling-calm-range-scaled-continuation
brief: 040_calm-downtrend-falls-keep-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f9d41455da54
---
Fidelity:
- Situation: a coin that has fallen over the last 3 days, in a falling calm market -> kept: the 3-day return is used, and only falls give a position (clipped to zero otherwise); the profile is added by code.
- Comparison: the fall in units of its 30-day average daily range, so larger falls bring more decline -> kept: the 3-day return is divided by the 30-day mean of (high − low)/close, and the position is graded by it.
- Outcome: keeps declining over the next 3 days, beyond the coin's usual drift -> kept: a short held for 3 bars, judged against the coin's drift.
- Verdict transfer: yes: the forecast measures the scaled 3-day fall exactly and shorts only it, inside the named profile, over the named horizon.
Forecast: The component is MeanAbsScaledReturnComponent with period 3, window 30 and base "mean_relative_range". It gives the 3-day return in multiples of the 30-day mean daily range. It is standardised against its own past 60 values (min_periods 20) and then clipped at max 0. So the forecast is 0 whenever the coin did not fall over 3 days. After a fall it is negative (short), and it grows in size linearly with the scaled fall, up to −20. It is never positive. The code keeps the book flat outside the falling calm profile.
Config: 040-02_falling-calm-range-scaled-continuation_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are short signals: a rise in the forecast's size of at least 2 points, read once per non-overlapping 3-bar grid cell. For each case, the unusual move is the coin's 3-bar return from the signal bar's close minus the coin's normal 3-bar drift over all windows, taken in the short direction. The measure is its mean and its t, with cases on the same day summed into one.
- Supporting check: Split the cases at the median of |forecast| on the signal bar. The top half's mean unusual move minus the bottom half's must be above 0. Its strength is Welch's t.
- Confirm: The main measure's t is 2 or more, and the supporting difference is above 0.
- Reject: The main measure's t is −2 or less (a rebound or no decline beyond drift), or the supporting difference has a Welch t of −2 or less (larger falls followed by less decline).
- Inconclusive: Any other result is inconclusive, including results near zero. A verdict needs at least 30 distinct case days across the coins and windows; with fewer, the test is inconclusive.
