---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's own daily fall that is large against its 20-day volatility -> adapted: "large" is made graded through a 1-day return in units of the 20-day return standard deviation, falls only, with a strong graded dead zone.
- Comparison: the fall in units of the usual daily move, where a larger fall means a larger rebound -> kept: VolatilityScaledReturnComponent(period 1, vol_period 20) measures exactly this, and position size grows with it.
- Outcome: the coin rises over the next 1 day -> kept: the position set at the fall bar's close is held over the next 1-day bar.
- Verdict transfer: yes: the test measures the volatility-scaled fall and the next-day rise as stated, on any weekday, and only the threshold is made graded.
Forecast: The forecast starts from the current daily return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). It is standardised over its own past 60 values (min_periods 20) and negated, so a fall is positive. It is clipped at 0, so it is zero on up days. It then passes through signed_power with exponent 3 and pivot 20, so ordinary falls give almost nothing. The result is a long position that is zero after rises and near zero after small falls. It grows steeply with the size of the volatility-scaled fall, up to +20 for the sharpest falls. It is never negative.
Config: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On every bar, take the position held after the trade (postRebalance_current_allocation) times the coin's next-bar excess return. The excess return is close[t+1]/close[t]-1 minus the coin's mean daily return over all its windows. Pool these products over all coins and windows. The measure is the t of their mean, before costs.
- Supporting check: On bars in the top 10% of positive forecasts (the largest volatility-scaled falls), the mean next-bar excess return is above 0.
- Confirm: The main measure has t ≥ 2 and the supporting check passes.
- Reject: The main measure has t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t ≥ 2 with a failed supporting check is also inconclusive. The test needs at least 300 bars with a non-zero position and at least 30 bars in the top-10% group; with fewer, it is inconclusive.
