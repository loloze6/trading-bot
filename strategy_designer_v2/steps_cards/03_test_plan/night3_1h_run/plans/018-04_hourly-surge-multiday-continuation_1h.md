---
idea: 018-04_hourly-surge-multiday-continuation
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 24h return at an hourly close first reaches several times the 30-day average absolute daily return, on the upside -> adapted: "first reaches" becomes "while", and the threshold becomes a graded size in multiples that is damped toward 0 below the extreme.
- Comparison: the coin's usual 5-day return -> kept: each case's 120-bar return is measured against the coin's mean 120-bar return over all windows.
- Outcome: the price rises over the next 5 days by more than usual, and more for larger multiples -> kept: the 120-bar forward return, held for 120 bars, read against the forecast's size.
- Verdict transfer: yes: the forecast is the idea's own multiple of the 30-day average absolute daily move, upside only, held for the idea's 5 days.
Forecast: The forecast starts from the coin's 24-bar percent return (PriceEvolutionComponent, period 24). Standardise divides it by the mean absolute 24-bar return over the previous 720 bars (30 days), times 10. The result is 10 per multiple of the usual daily move, capped at 20 (2 multiples). A clip at 0 removes the downside. A signed_power with exponent 3 and pivot 20 is the strongest graded dead zone the guide allows. Through it, 1 multiple gives about 2.5 and 1.5 multiples about 8.4. Two multiples or more give the full 20. The forecast is 0 whenever the 24h return is flat or negative and is never short. Its size grows smoothly with the multiple up to 2 multiples, then stays at the full size.
Config: 018-04_hourly-surge-multiday-continuation_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: The cases are the bars where the forecast rises by at least 2 points on the long side, read once per non-overlapping 120-bar grid cell of each window. For each case, take the coin's 120-bar forward return minus its mean 120-bar return over all windows. The measure is the mean of that unusual move, with its t-statistic.
- Supporting check: Across the cases, the slope of the unusual move on the forecast at the case's bar must be positive (larger multiples, larger rise).
- Confirm: The idea is confirmed only if both hold: - the mean unusual move is positive with t >= 2 over at least 30 cases; - the supporting check's slope is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any of these is inconclusive: - a t between -2 and 2; - t >= 2 with a slope at or below 0; - fewer than 30 cases pooled over the coins and windows.
