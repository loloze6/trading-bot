---
idea: 033-01_scaled-daily-fall-next-day-rebound
brief: 033_outsized-daily-fall-next-day-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's one-day fall, measured against the std of its daily returns over the past 30 days -> kept
- Comparison: the fall's size against the coin's own 30-day daily swing -> kept
- Outcome: the larger the fall, the larger the rise over the next day -> kept
- Verdict transfer: yes: the forecast is the fall in 30-day standard deviations, held for one day, so a rise that grows with it confirms the idea and its absence rejects it.
Forecast: The forecast comes from VolatilityScaledReturnComponent with period 1, vol_period 30, lag 0 and vol_lookback 1. Its raw value is today's return divided by the std of the last 30 daily returns. It is standardised over 60 past values (min_periods 20), then negated, then clipped at 0. The forecast is positive only on a down day, and it grows with the size of the fall in usual daily moves. It is 0 on up and flat days and is never short. A fall of about one usual move or more reaches the cap of 20.
Config: 033-01_scaled-daily-fall-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On bars with forecast > 0, the slope of the coin's next-day return (close[t+1]/close[t] - 1, within its window) minus its mean daily return over all windows (the drift). The slope is taken against the forecast. Its t is computed with cases on the same day summed into one piece of evidence.
- Supporting check: On those bars, the forecast-weighted mean of the next-day return minus drift must be above 0 with t ≥ 2, counted by day.
- Confirm: The slope's t is ≥ 2 and the supporting check passes (weighted mean excess return > 0, t ≥ 2).
- Reject: The slope's t is ≤ -2, or the weighted mean excess return has t ≤ -2.
- Inconclusive: Any other result, including slopes or means near zero with |t| < 2. A verdict needs at least 300 distinct days with forecast > 0 across the coins; with fewer, the result is inconclusive.
