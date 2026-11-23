---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: edf20a924da4
---
Fidelity:
- Situation: today's high-low range relative to its 30-day average range, wider is stronger -> kept: RangeCompressionRatioComponent, width form, today's range over the 30-day mean bar range.
- Comparison: only while the coin's own 20-day return is positive -> kept: a regime rule on the 20-day return being above 0; flat otherwise.
- Outcome: higher return over the next 5 days, rising with the range ratio -> kept: horizon of 5 daily bars, long.
- Verdict transfer: yes: the test measures this ratio, under this condition, against the 5-day return the idea names.
Forecast: The regime detector computes the coin's 20-day percent return. When that return is above 0, the bar is "trending". On every other bar the bar is "unknown" and the forecast is 0 (flat). On trending bars, the forecast comes from one component: today's high minus low, divided by the mean high-low range of the last 30 days (today included). It is standardised against its own past 60 values. The forecast is always positive in that regime, about +10 when the range is at its usual multiple, up to +20 when the range is far wider, and smaller when the range is narrow. So the long position grows with the range expansion, only while the 20-day rise lasts. When the 20-day return turns positive, the position starts at the level the range ratio gives; that jump is the idea's own condition.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use bars in the trending regime on the non-overlapping 5-bar grid of each window. For each, take the coin's 5-bar forward return minus the coin's normal 5-bar drift, measured over all its windows. Regress that excess return on the bar's forecast, pooled over coins, and read the t of the slope.
- Supporting check: On the same cases, the mean excess 5-bar return of the top third of forecasts minus that of the bottom third must be above 0.
- Confirm: The slope's t is 2 or more, and the top-minus-bottom-third difference is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a top-minus-bottom difference at or below 0. At least 100 trending-regime grid cases are needed; with fewer, the result is inconclusive.
