---
idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return -> adapted: "several times" becomes graded. The 24-bar return is divided by the mean absolute 24-bar return of the previous 720 bars, and only drops count.
- Comparison: the drop is measured in multiples of the 30-day average absolute daily return; the rise is judged against the coin's usual 1-day move -> kept: the first is the `standardise` divisor over 720 bars, the second is in the criterion.
- Outcome: the price rises over the next 1 day by more than the usual 1-day move, and more so for larger drops -> kept: 24-bar forward return, held 24 bars.
- Verdict transfer: yes: the forecast is the idea's own multiple of the drop, and the criterion tests both the size and the grading of the rise over the next day.
Forecast: The forecast starts from the 24-bar percent return (`PriceEvolutionComponent`, period 24). `standardise` with window 720 (30 days) divides it by the mean absolute 24-bar return of the 720 bars before the bar. The result is 10 per multiple of the coin's usual daily move, capped at 20. It is then negated so that drops read positive, and clipped at 0 so that rises give no position. Finally `signed_power` (exponent 3, pivot 20) damps it as the strongest graded dead zone. A drop of 1 multiple gives about 2.5, 1.5 multiples give about 8.4, and 2 or more multiples give 20 (fully long). The forecast is 0 on any bar whose 24-hour return is not a drop. It is never negative, and it grows smoothly with the size of the drop.
Config: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The strength of each case, averaged over all cases. A case is a bet, read once per 24-bar grid cell in each window. Its strength is the coin's 24-bar return from the signal bar, minus the coin's normal 24-bar drift over all windows, divided by the coin's usual 24-bar move. The usual move is the standard deviation of non-overlapping 24-bar returns. The measure is this mean strength minus 1, with its t over the cases.
- Supporting check: Across cases, the Spearman correlation between the case's forecast and its unusual move is above 0.
- Confirm: The mean strength minus 1 is above 0 with t >= 2, over at least 30 cases, and the Spearman correlation is above 0.
- Reject: The mean strength minus 1 is below 0 with t <= -2, over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming main measure with a correlation at or below 0 is also inconclusive. So is any result with fewer than 30 cases over all coins and windows.
