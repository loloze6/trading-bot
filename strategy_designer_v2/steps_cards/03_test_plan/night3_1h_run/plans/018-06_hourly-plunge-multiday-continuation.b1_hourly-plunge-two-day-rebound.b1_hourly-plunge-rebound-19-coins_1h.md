---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return -> adapted: the threshold "large multiple" becomes graded. The fall in multiples (24-bar return over the mean absolute 24-bar return of the prior 720 bars) is damped near zero and grows with the drop.
- Comparison: the rise is judged against the coin's usual 2-day drift -> kept: each case's 48-bar return minus the coin's mean 48-bar return over all windows.
- Outcome: the price rises over the next 2 days, more after a larger drop -> kept: each bet is held 48 bars, and its size grows with the drop in multiples.
- Verdict transfer: yes: the forecast measures the stated drop in the stated multiples, bets long for the stated 2 days, and is judged against the stated drift.
Forecast: One component, the 24-bar percent return (PriceEvolutionOnPeriodComponent, comparison_period 24). Standardise divides it by the mean absolute value of its previous 720 hourly readings, which is the 30-day average absolute daily return, with target 5 and cap 20. The standardised value is 5 x the move in daily multiples, capped at 4 multiples. It is negated, so drops read positive, and clipped at 0, so the forecast is long only and zero on rises. A signed_power with exponent 3 and pivot 20 then acts as the strongest dead zone. The forecast is 20 x (multiples / 4)^3: about 0.3 at a 1-multiple drop, 2.5 at 2, 8.4 at 3, and 20 at 4 or more. It is never negative and is near zero away from large drops.
Config: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The unusual move, measured on cases. A case is a rise of the forecast of at least 2 points, read once per cell of each window's non-overlapping 48-bar grid. The unusual move is the case's 48-bar return from the signal bar minus the coin's mean 48-bar return over all its windows, pooled over coins, with the t of its mean.
- Supporting check: Across cases, the slope of the unusual move on the forecast at the signal bar is positive (a larger drop in multiples gives a larger rise).
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting slope is positive.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, or a positive t >= 2 with a non-positive slope, or fewer than 30 cases.
