---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: edf20a924da4
---
Fidelity:
- Situation: a coin's daily high-low range on a given day -> kept
- Comparison: that range relative to its average range over the past 30 days, wider meaning stronger -> kept
- Outcome: the coin's return over the next 5 days is higher the wider the relative range -> kept
- Verdict transfer: yes: the forecast grades exactly the idea's ratio, and the test reads the 5-day return against it.
Forecast: The forecast starts from `RangeCompressionRatioComponent` with `short_period` 1, `long_period` 30, `base` "mean_bar_range" and `form` "width". Its raw value is today's high-low range divided by the mean daily range of the last 30 days, which is about 1 on a usual day. This ratio is standardised against its own 60 past values, so it sits near +10 at a usual range, about 20 at twice the usual range, and near 0 when the day is very narrow. A constant offset of -10 (`BuyAndHoldStrategy`, standardised, then negated) is averaged in with equal weight. The forecast is therefore (x − 10) / 2. It is 0 when today's range equals its usual size against the 30-day mean. It is positive and grows up to +5 as the range widens beyond that norm. It is negative, down to about -5, as the range narrows below it. It is graded on every bar, with no threshold.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The sample uses the bars at positions 0, 5, 10, ... of each window. For each, take the coin's 5-bar return from that bar's close minus the coin's mean 5-bar return over all its windows (its normal drift). Regress this excess return on the recorded `forecast`, pooled over coins and windows. The measure is the t of the slope.
- Supporting check: Split the book's mean daily return before costs into the part from the market's own rise and the rest. The part left after removing the market's own rise (timing) must be above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive, and so is a t of 2 or more with timing at or below 0. Fewer than 500 non-overlapping cases with a non-zero forecast is also inconclusive.
