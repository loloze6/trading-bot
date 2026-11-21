---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 1-day fall measured in its own 20-day daily volatility -> kept: the 1-bar return over the 20-bar return std, taken on falls only.
- Comparison: the rebound grows faster than the fall, so the largest falls carry most of it, against ordinary down days -> adapted: a graded convex weight replaces "buy only after rare outsized falls".
- Outcome: the price rises over the next 1 day -> kept: a long position held for 1 bar.
- Verdict transfer: yes: the forecast holds exactly the convex vol-scaled fall, and the criterion judges the next day's rise after the largest falls against smaller falls.
Forecast: The forecast starts from VolatilityScaledReturnComponent with period 1 and vol_period 20, which gives today's return in units of 20-day volatility. It is standardised against its last 60 values (min_periods 20). It is then negated, so falls read positive, and clipped at 0, so up days give 0 and the forecast is long only. Last, signed_power with exponent 3 and pivot 20 makes it strongly convex. A fall of average size gives a forecast near 1.25. A fall twice the average size, which reaches the cap of 20, gives a forecast of 20. The forecast is zero on up days and close to zero on ordinary down days. It grows as the cube of the fall's size.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take every bar with a forecast of 5 or more, pooled over all coins and windows. On each, compute the coin's next-day return close[t+1]/close[t]-1 minus that coin's mean daily return over all its windows. The measure is the one-sample t of the mean of these excess returns.
- Supporting check: The convexity check. The mean excess next-day return per unit of forecast must be larger in the group with forecast 5 or more than in the group with forecast between 0 and 5.
- Confirm: The main t is 2 or more, with at least 30 cases, and the supporting check passes.
- Reject: The main t is -2 or less, with at least 30 cases.
- Inconclusive: The idea is neither confirmed nor rejected in these cases: - the main t is between -2 and 2; - the main t is 2 or more but the convexity check fails; - there are fewer than 30 bars with a forecast of 5 or more.
