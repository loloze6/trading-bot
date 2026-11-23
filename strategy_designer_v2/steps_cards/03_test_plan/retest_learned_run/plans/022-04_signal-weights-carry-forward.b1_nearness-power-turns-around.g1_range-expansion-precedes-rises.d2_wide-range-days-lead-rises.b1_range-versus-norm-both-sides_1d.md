---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: the coin's daily high-low range against its 30-day average range -> kept: the day's range divided by the mean bar range over the last 30 bars, signed around that average.
- Comparison: wider or narrower than its 30-day norm, more strongly the further away -> kept: the forecast grows with the ratio's distance above or below its usual level of about 1.
- Outcome: the return over the next 3 days above the usual drift is higher after wider days and lower after narrower days -> kept: the 3-bar forward return minus the coin's mean 3-bar return.
- Verdict transfer: yes: the forecast is the idea's graded range-versus-norm reading, and the measure is the idea's 3-day excess return.
Forecast: The first component is RangeCompressionRatioComponent with short_period 1, long_period 30, base "mean_bar_range" and form "width". It gives today's high-low range divided by the mean bar range of the last 30 bars, which is about 1 on an average day. That value is standardised over 60 bars (min_periods 20), so it sits near +10 on a usual day, above 10 on wider days and below 10 on narrower days. A constant offset of -10 is added at equal weight. The forecast is therefore (x - 10) / 2: - it is positive (long) when the day is wider than its norm, up to about +5; - it is negative (lean against the coin) when the day is narrower, down to about -5; - it is about 0 on an average day; - it changes continuously with the distance from the norm.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: On each window's non-overlapping 3-bar grid, regress the coin's next 3-bar return (close[t+3]/close[t]-1) minus that coin's mean 3-bar return over all windows on the forecast at bar t. All coins and windows are pooled, and the result is the t of the slope.
- Supporting check: none
- Confirm: The slope is positive with t >= 2, over at least 1000 independent grid cases.
- Reject: The slope is negative with t <= -2, over at least 1000 independent grid cases.
- Inconclusive: A t between -2 and 2, or fewer than 1000 grid cases (about 5800 are expected: 6 coins x 24 windows x about 40 cells).
