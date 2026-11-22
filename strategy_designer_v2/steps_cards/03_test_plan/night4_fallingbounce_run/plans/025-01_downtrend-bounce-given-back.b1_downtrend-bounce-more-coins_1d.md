---
idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a one-day rise that is large against the 20-day standard deviation of daily returns, in a coin whose 90-day return is negative -> adapted: the 90-day fall is kept as a regime condition, and "large" is made graded, as the 1-day return in 20-day standard deviations, with a strong graded dead zone.
- Comparison: the rise is measured in units of the usual daily move, and the larger the rise, the larger the fall -> kept: the short size grows with the volatility-scaled rise.
- Outcome: a fall over the next 5 days -> kept: a short held 5 bars.
- Verdict transfer: yes: the forecast is the idea's scaled bounce, shorted only in falling coins over the idea's 5-day horizon.
Forecast: The forecast is zero on any bar where the coin's 90-day return is not negative. On a bar where it is negative, the forecast is computed as follows: - Input: the day's return divided by the 20-day standard deviation of daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). - Scale: that value is standardised against its own last 60 values (cap 20). - Up days only: it is clipped at 0, so that only rises count. - Dead zone: it is passed through signed_power with exponent 3 and pivot 20. This is the strongest graded dead zone the guide allows, so ordinary rises give almost nothing. - Direction: it is negated. The forecast is therefore never positive. It is zero on down days and outside falling coins, slightly negative on small rises, and grows short steeply as the bounce gets larger in usual daily moves, up to -20.
Config: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets, each a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close minus the coin's normal 5-bar drift over all its windows, in the short direction. The measure is the mean of that unusual move over all cases, with its t of the mean.
- Supporting check: The Pearson correlation, over the same cases, between the size of the forecast on the signal bar and the unusual move in the short direction is above 0.
- Confirm: The idea is confirmed when both hold: the mean unusual move is positive with t ≥ 2, and the supporting check's correlation is above 0.
- Reject: The idea is rejected when the mean unusual move in the short direction is negative with t ≤ -2, meaning bounces are followed by rises beyond the coin's normal drift.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t ≥ 2 with a correlation of 0 or below, and so is any result from fewer than 30 cases over all coins and windows.
