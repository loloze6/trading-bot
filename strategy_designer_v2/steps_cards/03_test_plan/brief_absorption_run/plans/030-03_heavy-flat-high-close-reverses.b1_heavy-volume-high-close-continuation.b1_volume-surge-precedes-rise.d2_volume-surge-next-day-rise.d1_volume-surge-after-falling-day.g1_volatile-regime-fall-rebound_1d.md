---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 91c94c46188e
---
Fidelity:
- Situation: a one-day fall measured in usual daily moves, larger falls stronger -> kept: the 1-bar return over the 20-day return std, negated and kept on falls only.
- Comparison: 20-day volatility against its own mean over the past 120 days, more elevated stronger -> adapted: "refuse in calm periods" becomes a graded weight s(t)/mean(s over 120), small when calm.
- Outcome: the coin rises over the next day -> kept: forecast long, horizon 1 bar.
- Verdict transfer: yes: the forecast is exactly the fall in usual moves times the volatility ratio, so a next-day rise that grows with it confirms the idea, and a fall that grows with it rejects it.
Forecast: The forecast uses one indicator, VolatilityScaledReturnComponent with period 1, vol_period 20 and vol_lookback 120. Its raw value is the day's return divided by the mean of the 20-day return std over the last 120 days. This equals the fall in usual daily moves (one 20-day std) times the 20-day std over its own 120-day mean. - The value is standardised against its past 140 values, then negated, so a fall reads positive. - It is then clipped at 0, so the forecast is long only. - It is 0 on up days and flat days. - It grows in proportion to the depth of the fall and to how far volatility stands above its 120-day norm. - A fall in calm periods gives a small position.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope, from a pooled least-squares regression over all coins and windows, of the next-day return on the bar's forecast. The return is close[t+1]/close[t]-1 minus the coin's mean daily return over all windows. The regression uses the bars with forecast > 0, one case per bar, inside windows only.
- Supporting check: The mean next-day excess return (as above) over the bars in the top third of positive forecasts is above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with |t| < 2 is inconclusive, as is a positive slope with t ≥ 2 when the top-third mean is not above 0. Fewer than 300 bars with forecast > 0 across all coins and windows is also inconclusive.
