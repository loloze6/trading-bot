---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, after closing below it the day before -> adapted: "several times" is graded by the touch count N of the crossed swing-high level (90 bars, 2% band, one-bar cross), times the close's margin above it.
- Comparison: the more times it turned down there, the larger the rise -> kept: the forecast grows with the level's touch count.
- Outcome: the price rises over the next 3 days -> kept: each bet is held 3 bars and judged on the 3-bar return.
- Verdict transfer: yes: the forecast is non-zero only on the bars of this break and grows with the level's turn count, so the 3-bar result after it answers the idea both ways.
Forecast: The forecast uses ResistanceBreakTouchCountComponent (period 90, side 2, band 2.0, cross_period 1). On a bar whose close crosses up through a 90-day swing-high close, after closing at or below it the day before, it reads N x the percent margin above the level. N is the number of turns down within 2% of that level. On every other bar it reads 0. It is standardised against its own past 90 values, so a typical break reads about 10, capped at 20. It is never negative, so the strategy is long only. It is 0 when there is no fresh break, and it grows with the level's turn count and with how clearly the close cleared it.
Config: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Cases are rises of the forecast of at least 2 points, counted once per cell of the 3-bar grid of each window. For each case, take the coin's 3-bar return from the case's close minus the coin's mean 3-bar return over all windows (its drift). The measure is the mean of this excess over the cases, pooled over coins, with its t over the cases.
- Supporting check: Across the cases, regress the excess 3-bar return on the forecast's size at the case bar (`post_pipeline_value`). The slope must be positive.
- Confirm: The mean excess 3-bar return is positive with t >= 2, and the supporting slope is positive.
- Reject: The mean excess 3-bar return is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive mean with t >= 2 but a slope of 0 or below is also inconclusive. So is any result with fewer than 30 cases.
