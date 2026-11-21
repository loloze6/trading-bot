---
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: 24h return first reaches several times its 30-day average absolute daily return, upside, at an hourly close -> adapted: "first reaches" becomes "while", and "several times" becomes a graded size in usual daily moves with the strongest graded dead zone.
- Comparison: only while the close stands near its 30-day high, closer giving a larger rise; and more than the coin's usual 5-day return -> kept: a proximity weight to the 720-bar closing high, with the coin's normal 120-bar drift removed in the criterion.
- Outcome: price keeps rising over the next 5 days -> kept: a long position held 120 bars.
- Verdict transfer: yes: the forecast is the idea's own surge in usual daily moves times its nearness to the 30-day high, judged over its own 5-day horizon against the coin's usual 5-day move.
Forecast: The forecast uses HighProximityScaledReturnComponent (period 720, return_period 24, window 720, power 2). Its raw value is the 24-hour return in multiples of the 30-day mean absolute 24-hour return, times (1/(1+D))^2. D is the percent distance of the close below its 720-bar closing high, so the weight is 1 at the high and shrinks below it. The raw value is standardised against its own past 500 values and clipped at 0, so only upside surges count. Then signed_power (exponent 3, pivot 20) applies the strongest graded dead zone: ordinary hours stay near 0, and the position grows steeply as the surge grows and the close nears the month's high. The forecast is never negative, is 0 when the 24-hour return is not positive, and runs on every bar with no regime.
Config: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: For each case, take the coin's 120-bar return from the signal bar's close minus the coin's normal 120-bar drift. A case is a long bet, a forecast rise of at least 2 points, read once per non-overlapping 120-bar grid cell of each window. The measure is the mean of these unusual moves over all coins and windows, with the t of that mean.
- Supporting check: The mean unusual move of the cases in the upper half of the signal-bar forecast minus that of the lower half is above 0.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a positive t >= 2 whose supporting check fails, or fewer than 30 cases.
