---
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: the 24h return at an hourly close first reaches several times the 30-day mean absolute daily return, upside, near the 30-day high -> adapted: the 24h return measured in usual daily moves, weighted by nearness to the 30-day closing high; "first reaches several times" becomes a graded "while" with a strong dead zone.
- Comparison: the coin's usual 5-day return -> kept: the 120-bar returns after the cases, minus the coin's normal 120-bar drift.
- Outcome: the price keeps rising over the next 5 days, more the closer the close is to its high -> kept: 120-bar forward return, long side, sized by the proximity-weighted surge.
- Verdict transfer: yes: the forecast is the proximity-weighted surge itself, and the criterion measures the 5-day excess rise that follows it.
Forecast: One indicator, HighProximityScaledReturnComponent with period 720 (30-day closing high), return_period 24 (24h return), window 720 (30-day mean absolute daily return) and power 2. It is the 24h return in usual daily moves, times a weight that is 1 at the 30-day high and shrinks the further the close sits below it. It is standardised against its own past 500 values and clipped at 0, so the forecast is long only. A signed_power step with exponent 3 and pivot 20 then damps ordinary values to near 0, so only multi-move surges near the high give a sizeable long. The forecast is zero on falls and grows steeply with the size of the surge and with closeness to the high.
Config: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: A case is a long-side rise of the forecast of at least the band, counted once per 120-bar grid cell of each window. For each case, take the 120-bar return from the signal's close minus the coin's normal 120-bar drift (its mean over all windows). Average this unusual move over all cases and coins, and compute its t-statistic.
- Supporting check: The mean unusual move of cases in the upper half of entry forecast, minus that of cases in the lower half, is above 0.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 independent cases, and the supporting check is above 0.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 independent cases.
- Inconclusive: Any other result, including a t between -2 and 2, or a confirming t whose supporting check fails. Fewer than 30 cases is always inconclusive.
