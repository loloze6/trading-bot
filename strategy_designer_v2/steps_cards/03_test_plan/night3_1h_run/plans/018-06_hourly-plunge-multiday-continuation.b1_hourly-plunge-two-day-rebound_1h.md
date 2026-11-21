---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: 24-hour return, read at an hourly close, falls by a large multiple of the 30-day average absolute daily return -> adapted: the 24-bar return divided by the mean absolute 24-bar return of the previous 720 bars, graded; drops only.
- Comparison: the coin's usual 2-day drift -> kept
- Outcome: price rises over the next 2 days, more for larger drops -> kept
- Verdict transfer: yes: the forecast grows with the same drop-in-multiples the idea names and is judged on the 48-bar rise against the coin's drift.
Forecast: One component, the 24-bar percent return (`PriceEvolutionComponent`, period 24). It is standardised over a 720-bar window: the latest return times 10, divided by the mean absolute 24-bar return over the previous 720 hours. That mean is the coin's 30-day average absolute daily return, so a reading of 10 is a one-multiple move, and the output is capped at ±20, which is two multiples. The value is then negated, so a drop reads positive. It is clipped at 0, so rises give no position. Last, it is passed through `signed_power` with exponent 3 and pivot 20, the strongest graded dead zone. A drop of 0.5 multiple gives about 0.02. One multiple gives 2.5. One and a half multiples give 8.4. Two multiples or more give 20. The forecast is never negative and is 0 when the 24-hour return is not negative. It grows continuously with the size of the drop in multiples of the usual daily move.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the bars where the forecast rises by at least 2 points, read once per 48-bar grid cell of each window. For each case, take the coin's return from the close of that bar over the next 48 bars, inside the window, and subtract the coin's mean 48-bar return over all its windows (non-overlapping grid). The measure is the mean of these excess returns over all cases and coins, with the t of that mean.
- Supporting check: Over the same cases, the Spearman correlation between the forecast at the case bar and its 48-bar excess return is above 0. This checks that larger drops give larger rises.
- Confirm: The mean excess return is above 0 with t ≥ 2, and the supporting correlation is above 0.
- Reject: The mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 with a correlation of 0 or less. So is any result from fewer than 30 cases over all coins and windows.
