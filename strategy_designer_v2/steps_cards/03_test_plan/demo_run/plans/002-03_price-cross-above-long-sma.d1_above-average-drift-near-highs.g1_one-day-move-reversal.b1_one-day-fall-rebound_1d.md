---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's one-day fall, the larger the stronger -> kept
- Comparison: the fall relative to the standard deviation of daily returns over the past 20 days -> kept
- Outcome: a larger rise over the next day -> kept
- Verdict transfer: yes: the forecast grows with the 20-day-volatility-scaled one-day fall and is held exactly one bar, so the result decides the idea.
Forecast: The forecast starts from `VolatilityScaledReturnComponent` with `period` 1 and `vol_period` 20. This is today's return divided by the standard deviation of the last 20 daily returns. The value is standardised against its past 60 values and then negated, so a fall becomes positive. It is then clipped at 0 from below, which keeps only the falls. The forecast is 0 on up days. On down days it is positive, and it grows in proportion to the size of the fall in units of the coin's usual move: a 1-sigma fall gives about +12 and a 2-sigma fall about +20, the cap. The forecast is never negative. The position is set at the close and held to the next close, which is the one-day hold.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast > 0, pooled over all coins and windows. On each bar, take the position held after the trade, multiplied by the next-day excess return. The excess return is close[t+1]/close[t] - 1 minus the coin's mean daily return over all windows. Report the t of the mean of this product, with the number of bars.
- Supporting check: Among the bars with forecast > 0, compare the top quintile of forecast with the bottom quintile. The check passes if the mean next-day excess return of the top quintile minus that of the bottom quintile is greater than 0.
- Confirm: The main measure gives t >= 2 with at least 100 positive-forecast bars, and the supporting check passes.
- Reject: The main measure gives t <= -2 with at least 100 positive-forecast bars.
- Inconclusive: These results neither confirm nor reject: - t between -2 and 2; - t >= 2 while the quintile difference is <= 0; - fewer than 100 positive-forecast bars.
