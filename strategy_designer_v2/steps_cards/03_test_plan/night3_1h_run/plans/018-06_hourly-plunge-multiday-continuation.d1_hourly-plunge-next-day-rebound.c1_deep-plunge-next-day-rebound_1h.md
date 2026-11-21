---
idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return -> kept: the 24-bar return is divided by the mean absolute 24-bar return over the prior 720 bars.
- Comparison: the rise is judged against the coin's normal 1-day drift -> kept: the criterion subtracts the coin's mean 24-bar return over all windows.
- Outcome: the price rises over the next 1 day, more the larger the drop -> kept: each bet is held 24 bars and sized by the drop's multiple, up to 2 multiples where the forecast caps.
- Verdict transfer: yes: the drop is measured as stated and each bet is held 24 bars, so this test confirms or rejects the idea directly.
Forecast: One component, PriceEvolutionComponent with period 24, gives the coin's 24-hour return in percent. standardise with window 720 divides it by the mean absolute 24-hour return of the 720 bars before the current one (30 days), times 10. The value is therefore 10 times the drop's multiple of the usual daily move, capped at ±20 (2 multiples). It is then negated and clipped at 0, so only drops give a value: positive, and zero after any rise. signed_power with exponent 3 and pivot 20 then damps it into a strong graded dead zone. A 1-multiple drop gives about 2.5 (a 25 % long). A 1.5-multiple drop gives about 8.4. A drop of 2 multiples or more gives 20 (a 200 % long). The forecast is never negative and is zero when the coin did not fall over the last 24 hours.
Config: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are bets: a rise of the forecast of at least 2 points, read once per non-overlapping 24-bar grid cell of each window. For each case, take the coin's 24-bar return from the signal's close minus the coin's normal 24-bar drift (its mean over all windows). Pool these excess returns over coins and windows, and compute their mean and its t, before costs.
- Supporting check: Split the cases by forecast at the signal bar: at least 10 against below 10. The mean excess return of the first group minus that of the second must be above 0 (Welch).
- Confirm: The mean excess 24-bar return is positive with t ≥ 2 over at least 30 cases, and the supporting difference is above 0.
- Reject: The mean excess 24-bar return is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a non-positive supporting difference is inconclusive. Fewer than 30 cases is inconclusive.
