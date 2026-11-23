---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: the daily high-low range is wide relative to its 30-day average range -> kept: the 1-day range over the mean bar range of the last 30 bars, as a continuous ratio.
- Comparison: only while the 20-day return is positive, judged against the coin's usual return -> kept: a regime rule (20-day return > 0) selects the bars, and the outcome is judged against holding the coin.
- Outcome: the wider the range, the higher the return over the next 10 days -> kept: the 10-day forward return, rising with the range ratio.
- Verdict transfer: yes: the test measures this range ratio, inside this condition, against this horizon, so a confirm or a reject applies to the idea as stated.
Forecast: The regime detector reads the 20-day percent return (`PriceEvolutionOnPeriodComponent`, 20). When that return is above 0, the bar is `trending`. Otherwise it is `unknown`, which is flat. On trending bars, the forecast is today's high-low range divided by the mean high-low range of the last 30 bars (`RangeCompressionRatioComponent` with short_period 1, long_period 30, base "mean_bar_range", form "width"). That ratio is standardised over its past 60 values. The forecast is always long: about +10 when today's range is at its usual ratio to the 30-day average, larger up to +20 as the range widens, and smaller as it narrows. It is zero outside a 20-day rise. The condition is the idea itself, so the position can jump from zero at the regime's edge. Inside the regime the size is graded by the range ratio.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are the bars at positions 0, 10, 20, ... of each window where the regime is `trending` and the forecast is above 0. For each case, take the coin's 10-day return from that close, minus the coin's mean 10-day return over all its windows. Pool these excess returns over all coins and regress them on the forecast. The measure is the t of the slope.
- Supporting check: The mean excess 10-day return of the cases whose forecast is above the in-regime median is above 0, so the gain is not just the market's own rise.
- Confirm: The slope t is 2 or more, and the supporting check passes.
- Reject: The slope t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a slope t of 2 or more with the check failing, is inconclusive. Fewer than 100 in-regime cases in total, or fewer than 30 on either side of the median, is also inconclusive.
