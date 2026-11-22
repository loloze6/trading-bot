---
idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise of several usual daily moves (day's return over the std of the last 20 daily returns) -> adapted: the "several moves" threshold is made graded, as the rise in usual moves clipped at 0 with the strongest graded dead zone; "after" the rise becomes "while" it is the signal bar, and the bet is held for 20 bars.
- Comparison: the 90-day return negative versus positive -> kept: a regime splits bars on the sign of the 90-day return.
- Outcome: the 20-day return is lower in the falling group, and the gap widens with the rise -> kept: 20-day forward returns compared between the groups, and against the size of the rise.
- Verdict transfer: yes: the test measures the same rise, the same split and the same 20-day gap, so its verdict is the idea's.
Forecast: The rise is the day's return in usual moves (`VolatilityScaledReturnComponent`, period 1, vol_period 20). It is standardised over 60 bars, clipped at 0 so only rises count, then damped with `signed_power` (exponent 3, pivot 20). An ordinary up day gives nearly 0, and a rise of several usual moves gives up to +20. The regime detector reads the 90-day return (`PriceEvolutionComponent`, period 90). When it is at or above 0, the bar is "trending" and the forecast is +rise: long, larger the sharper the rise. When it is below 0, the bar is "mean_reversion" and the forecast is -rise: short, larger the sharper the rise. The forecast is zero on down days and close to zero on small rises.
Config: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Cases are bets (forecast rises of at least 2 points), read once per 20-bar grid cell of each window. For each case, take the coin's 20-bar return from the signal bar's close minus the coin's normal 20-bar drift. Compare the mean over trending cases with the mean over mean_reversion cases, as trending minus mean_reversion, with Welch's t. This is judged before costs and against holding the coin.
- Supporting check: Split the cases at their median |forecast|. The gap (trending minus mean_reversion unusual move) must be larger among the larger-rise cases than among the smaller-rise cases.
- Confirm: The gap is positive with Welch t >= 2, and the supporting check passes (the larger-rise gap exceeds the smaller-rise gap).
- Reject: The gap is negative with Welch t <= -2: after sharp rises, coins down over 90 days do better than coins up over 90 days.
- Inconclusive: Any t between -2 and 2, or t >= 2 when the supporting check fails, is inconclusive. So are fewer than 30 cases in either group.
