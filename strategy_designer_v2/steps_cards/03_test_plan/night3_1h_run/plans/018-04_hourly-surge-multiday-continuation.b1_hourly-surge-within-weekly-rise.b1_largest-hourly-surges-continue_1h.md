---
idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return, on the upside -> adapted: the ratio is graded rather than a threshold, and "first reaches" becomes "while it is high"; long only, with a cubic dead zone.
- Comparison: a rise larger than the coin's usual 5-day return, only while the 7-day return is positive -> kept: the usual 5-day return is the coin's normal drift in the criterion, and the 7-day condition is a regime.
- Outcome: the price keeps rising over the next 5 days, more after larger surges -> kept: held 120 bars, size grows with the ratio.
- Verdict transfer: yes: the forecast is the idea's own ratio, under its own 7-day condition, judged over its own 5 days against the coin's usual move.
Forecast: The 24-bar return (`PriceEvolutionComponent`, period 24) is standardised over 720 bars. This divides it by its mean absolute value over the prior 30 days, so 10 means one usual daily move and 20 (the cap) means twice that. It is clipped at 0 (up surges only). It then goes through `signed_power` with exponent 3 and pivot 20: a usual move gives 2.5, 1.6 times usual gives about 10, and twice usual or more gives 20. The forecast is long only, near zero for ordinary moves and steeply larger for surges. It is active only while the 168-bar return is positive (regime `trending`). Otherwise the regime is `unknown`, which is null, so the forecast is 0.
Config: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: Cases are bets: rises of the forecast of at least 2 points, read once per non-overlapping 120-bar grid cell. For each case, take the coin's 120-bar return from the signal's close minus the coin's normal 120-bar drift over all windows. Measure the mean of that excess, pooled over coins, with the t of the mean.
- Supporting check: The mean excess of cases with a forecast of 10 or more (surges of about 1.6 times usual or more) is larger than that of cases below 10 (Welch difference above 0).
- Confirm: The mean excess is above 0 with t ≥ 2 and at least 30 cases, and the supporting check passes.
- Reject: The mean excess is below 0 with t ≤ -2 and at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is t ≥ 2 when the supporting check fails, or fewer than 30 cases.
