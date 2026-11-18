---
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a higher 10-day return, and a close nearer the top of its prior 20-day range -> kept
- Comparison: none (a graded relation, stronger situation means a larger rise) -> kept
- Outcome: price rises further over the next 10 days, upward -> kept
- Verdict transfer: yes: the forecast grows with exactly the two quantities named, and is judged on the 10-day forward return.
Forecast: The forecast is the equal-weight mean of three parts, each standardised over 60 bars with min_periods 20. - The 10-bar percent return (PriceEvolutionComponent, period 10). It is positive after a rise and grows with its size. - The percent distance of the close from the highest high of the 20 bars before the current bar (DistanceFromHighComponent, period 20, source high, exclude_current 1). It is mostly negative, about -10 on average after standardising, and rises toward 0 and above as the close nears or breaks the prior top. - A constant +10 (BuyAndHoldStrategy). It centres the distance term, which is then positive when the close is nearer the prior 20-day top than usual and negative when further below it. So the forecast is (momentum + distance + 10) / 3. It is positive and larger the stronger the 10-day return and the nearer the close sits to the prior top. It is negative when both are weak, and near 0 when they are average or offset each other. The forecast is signed and continuous, with no regime and no dead zone, because the idea is a steady graded relation.
Config: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On a non-overlapping 10-bar grid in each window, regress the coin's 10-bar forward return on the forecast at t, pooled over coins and windows. The forward return is measured in excess of that coin's mean 10-bar return over all windows. The measure is the t of the slope.
- Supporting check: The mean excess 10-bar return of the top forecast quintile minus that of the bottom quintile is above 0.
- Confirm: The slope t is 2 or more and the top-minus-bottom quintile difference is above 0.
- Reject: The slope t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a quintile difference of 0 or below. At least 300 independent grid cases are required (about 1,700 expected); with fewer, the result is inconclusive.
