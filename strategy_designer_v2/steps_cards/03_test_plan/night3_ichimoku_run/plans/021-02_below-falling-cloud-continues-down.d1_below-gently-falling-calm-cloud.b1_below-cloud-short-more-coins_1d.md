---
idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: a31b77de3651
---
Fidelity:
- Situation: the coin closes below its Ichimoku cloud while the cloud is falling -> adapted: "after" made "while". A regime rule fires on bars where the close sits below the cloud's lower edge and the 26-day cloud slope is below 0.
- Comparison: a slower 26-day cloud fall and calmer 30-day daily moves give a larger short -> kept. The short size shrinks steadily as the 26-day cloud-slope size and the 30-return volatility grow.
- Outcome: the coin's return over the next 26 days is negative -> kept. The test is a short held for 26 bars.
- Verdict transfer: yes: the test measures the same cloud, the same slope and volatility windows, the same direction and the same 26-day horizon.
Forecast: - When it is active: only on bars where the close is below the cloud (IchimokuCloudPositionComponent, 9/26/52/26, nearest edge) and the cloud's mid level has fallen over 26 bars (IchimokuCloudSlopeComponent, lookback 26). On every other bar the forecast is 0. - Its parts on those bars: - s: the cloud slope, standardised and negated. It is positive, about 10 for a usual fall and larger for a steeper one. - v: the standard deviation of the last 30 daily returns, standardised. It is positive, about 10 when volatility is at its usual level. - A constant -10 with weight 4. - How they combine: forecast = (-40 + v + s) / 6. - Its range: always short or flat, from about -6.7 (flat cloud, very calm coin) to 0 (both at their cap of 20). It is about -3.3 when both are at their usual level. The short shrinks steadily as either the fall or the volatility grows.
Config: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: On the grid of every 26th bar of each window, take the bars where the forecast is below 0. For each, compute -forecast/10 x (the coin's 26-bar forward return minus its mean 26-bar return over all windows). This is the short's gain beyond holding the coin. Report its mean and t, with the number of cases.
- Supporting check: Among those cases, the mean of (forward return minus drift) for the cases with |forecast| above the median, minus the same mean for the cases below the median, must be below 0.
- Confirm: The main mean is positive with t >= 2 over at least 30 cases, and the supporting difference is below 0.
- Reject: The main mean is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a supporting difference of 0 or above is also inconclusive. So is any result from fewer than 30 non-overlapping cases.
