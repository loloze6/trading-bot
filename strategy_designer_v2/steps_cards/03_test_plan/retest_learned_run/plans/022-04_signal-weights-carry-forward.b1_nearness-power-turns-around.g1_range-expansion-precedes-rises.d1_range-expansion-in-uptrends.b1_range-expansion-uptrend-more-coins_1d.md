---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a coin's daily high-low range, relative to its 30-day average range, while its own 20-day return is positive -> kept: bar t's range over the mean bar range of the last 30 bars, graded, with a regime on 20-day return > 0
- Comparison: the average daily range over the past 30 days -> kept
- Outcome: a higher return over the next 5 days, the wider the range -> kept: held 5 bars, with gains judged by forecast size
- Verdict transfer: yes: every part is measured as stated, so a confirm or a reject of this forecast is a confirm or a reject of the idea.
Forecast: The regime is "trending" while the coin's 20-day close-to-close return (PriceEvolutionComponent, period 20) is above 0. On every other bar the forecast is 0 (flat). In the trending regime the forecast is the ratio of bar t's high-low range to the mean high-low range of the last 30 bars, bar t included (RangeCompressionRatioComponent: short_period 1, long_period 30, base "mean_bar_range", form "width"). It is standardised over its 60 past values (min_periods 20). The forecast is therefore always long inside the regime. It is about +10 when the range ratio is at its usual size, grows smoothly toward +20 as the day's range widens beyond its 30-day norm, and shrinks toward 0 as the range narrows. No constant offset is added, because a constant inside a regime is not allowed.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, on bars in the trending regime with forecast > 0. For each case, take the 5-bar forward return minus the coin's mean 5-bar return over all its windows. Compare the cases with forecast above the median of those cases against the cases at or below it: the difference upper minus lower, with Welch's t.
- Supporting check: The mean excess 5-bar return (over the coin's mean) of the upper-half cases is above 0.
- Confirm: The difference is above 0 with Welch t ≥ 2, and the supporting check passes.
- Reject: The difference is below 0 with Welch t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t of 2 or more when the supporting check fails, and so is a run with fewer than 30 cases in either half.
