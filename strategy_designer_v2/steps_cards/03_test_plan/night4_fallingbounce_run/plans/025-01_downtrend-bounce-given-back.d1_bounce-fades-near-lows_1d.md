---
idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: in a coin with a negative 90-day return, a one-day rise that is large against its 20-day standard deviation of daily returns. -> adapted: the 90-day condition is kept as a regime; "large" is made graded as the day's rise counted in usual moves.
- Comparison: the closer the close is to its lowest close of the past 90 days, the larger the fall. -> kept: the rise is weighted by 1/(1 + percent distance above the 90-day closing low).
- Outcome: the price falls over the next 5 days. -> kept: a short position, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's bounce, sized by nearness to the low, shorted only while the 90-day return is negative, and judged on the next 5 days.
Forecast: The forecast is active only while the coin's 90-day percent return is below 0 (regime `mean_reversion`); on all other bars it is flat. - Measure. On active bars it is LowProximityScaledRiseComponent (vol_period 20, period 90). This is the day's rise divided by the 20-day standard deviation of daily returns, 0 on down days, times 1/(1 + percent distance of the close above its 90-day closing low). - Transforms. It is standardised over its past 90 values (min_periods 22). It is then damped with signed_power (exponent 3, pivot 20), the strongest graded dead zone, because a large bounce near the low is rare. It is then negated. - Sign and size. The forecast is 0 or negative. It is more negative the larger the bounce and the nearer the close is to the 90-day low. It is near zero for small bounces and for bounces far above the low.
Config: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Per case, the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift (holding the coin, all windows together), in the short direction. A case is a short bet, a fall of the forecast of at least 2 points, read once per 5-bar grid cell. The measure is the mean of that unusual move over all coins' cases, with its t.
- Supporting check: Split the cases at the median absolute forecast of the bet bar. The mean unusual move of the larger half minus that of the smaller half must be above 0, so that the fall grows with the bounce and with nearness to the low.
- Confirm: The mean unusual move is positive, a fall after bounces, with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative, a rise after bounces, with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming t with a failed supporting check. So is any result from fewer than 30 cases.
