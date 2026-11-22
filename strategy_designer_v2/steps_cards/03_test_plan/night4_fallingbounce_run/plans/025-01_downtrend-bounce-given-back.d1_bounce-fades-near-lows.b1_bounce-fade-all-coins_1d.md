---
idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise that is large against the 20-day standard deviation of daily returns, in a coin whose 90-day return is negative -> adapted: the rise threshold is made graded (the rise in usual moves, clipped at 0); "90-day return negative" is kept as a regime condition.
- Comparison: the closer the close sits to its lowest close of the past 90 days, the larger the fall -> kept: the rise is weighted by 1/(1+D), D being the percent distance above the 90-bar closing low.
- Outcome: the price falls over the next 5 days -> kept: a short bet held 5 bars.
- Verdict transfer: yes: the forecast is the idea's own rise × proximity measure, applied only in falling coins, short over its own 5-day horizon.
Forecast: The forecast is computed only while the coin's 90-bar return is below 0 (the regime `mean_reversion`). On all other bars it is 0, flat. In that regime it uses LowProximityScaledRiseComponent (vol_period 20, period 90). This is today's rise divided by the 20-day standard deviation of daily returns, clipped at 0, times 1/(1 + percent distance of the close above its 90-day closing low). The value is standardised (window 90, min_periods 22) and passed through the strongest graded dead zone (signed_power, exponent 3, pivot 20), so ordinary bars sit near 0. It is then negated. The forecast is therefore 0 on down bars and never positive. It goes more negative (a larger short) the bigger the bounce in usual moves and the nearer the close still is to the 90-day low.
Config: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all its windows, in the short direction. The measure is the mean of this unusual move over all cases, with its t-statistic.
- Supporting check: Across cases, the slope of the unusual move (short direction) on |forecast| at the signal bar is above 0. Larger bounces nearer the low should fall more.
- Confirm: The mean unusual move is positive with t ≥ 2 over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean unusual move is negative with t ≤ -2 over at least 30 cases: the price rises after these bounces, beyond its drift.
- Inconclusive: Any t between -2 and 2, or a confirming t with a slope ≤ 0, or fewer than 30 cases.
