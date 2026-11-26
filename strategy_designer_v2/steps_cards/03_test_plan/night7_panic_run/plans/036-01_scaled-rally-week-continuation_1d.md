---
idea: 036-01_scaled-rally-week-continuation
brief: 036_scaled-rallies-continue-next-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's 3-day rise that is large against its usual daily swing (30-day std of daily returns) -> adapted: the unnamed "large" made graded: scaled 3-day rise, long side only, under the strongest graded dead zone (cube)
- Comparison: the 3-day return against the 30-day std of daily returns -> kept
- Outcome: the coin keeps rising over the next 7 days, more after larger scaled rises -> kept
- Verdict transfer: yes: the forecast is the idea's scaled rise, held for its 7 days, and both the gain and its growth with size are measured.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 3 and vol_period 30. It is the 3-day return divided by the std of the last 30 daily returns (times sqrt 3, a constant). It is standardised against its own last 60 values and clipped at 0, so it is long only. A signed_power with exponent 3 is then applied. The forecast is 0 after a 3-day fall. It is near 0 after an ordinary rise, for example 1.25 at half the usual size. It grows steeply with larger scaled rises: 10 at the usual size, and capped at 20 from about 1.3 times the usual size.
Config: 036-01_scaled-rally-week-continuation_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Each case is a bet: the forecast rises by at least 2 points, read once per 7-bar grid cell. For each case, take the coin's 7-bar return from the signal bar's close minus the coin's normal 7-bar drift (holding the coin). The measure is the mean of this unusual move, with its t, the cases of one day taken together.
- Supporting check: Across the cases, regress the unusual move on the forecast at the signal bar. The slope must be positive.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting slope is above 0.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any other result is inconclusive: t between -2 and 2, or a confirming mean with a slope of 0 or below. It is also inconclusive with fewer than 30 distinct case days over all coins and windows.
