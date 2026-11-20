---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's fall over the 24 hours up to the 20:00 UTC close, while its 10-day hourly volatility is high -> adapted: the 20:00 close and "volatility high" (10-day volatility above its 30-day average) gate a regime; the 24h fall times that volatility ratio is graded.
- Comparison: larger rise the higher the volatility, and beating holding the coin -> kept: the forecast grows with the volatility ratio, and the gain is judged against holding.
- Outcome: the coin rises over the next 24 hours -> kept: the long is held 24 hourly bars.
- Verdict transfer: yes: the test takes the long at the 20:00 close on high-volatility days, sizes it by fall and volatility, and holds it for the idea's 24 hours.
Forecast: The forecast is computed only on the bar that closes at 20:00 UTC, and only when the 240-bar volatility of hourly returns is at or above its 720-bar average; on every other bar it is 0. On those bars the indicator is `VolatilityScaledReturnComponent` (period 24, vol_period 240, vol_lookback 720). It gives the 24-hour return in usual moves times current volatility over its 30-day average. It is negated, so a fall reads positive, and standardised over its past 500 hourly values (min_periods 120). It is clipped at 0, so the trade is long only. The forecast is 0 after a rise. It grows with the depth of the 24-hour fall and with how far volatility sits above its average.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use the bars where `regime` is mean_reversion and the forecast is above 0, one case per coin-day, pooled over coins and windows. For each case, take forecast/10 × (close[t+24]/close[t] − 1 − the coin's mean 24-bar return over all windows). Measure the t of the mean of these values.
- Supporting check: Over the same cases, the OLS slope of the excess 24-bar return on the forecast is above 0.
- Confirm: t ≥ 2 with at least 100 cases, and the slope is above 0.
- Reject: t ≤ −2 with at least 100 cases.
- Inconclusive: −2 < t < 2, or t ≥ 2 with a slope at or below 0, or fewer than 100 cases.
