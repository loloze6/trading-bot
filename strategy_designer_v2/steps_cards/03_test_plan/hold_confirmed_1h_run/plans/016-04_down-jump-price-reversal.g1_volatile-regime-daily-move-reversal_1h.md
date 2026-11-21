---
idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: 24-hour return measured in units of past 7-day hourly volatility -> kept: VolatilityScaledReturnComponent with period 24 and vol_period 168 (the 7-day window includes bar t).
- Comparison: reversal stronger the higher 7-day volatility is against its usual level -> kept: vol_lookback 720 multiplies the scaled return by s(t) / mean(s over 720 bars), so the fade grows with relative volatility.
- Outcome: price moves the opposite way over the next 24 hours -> kept: the forecast is negated and judged on the next 24 bars.
- Verdict transfer: yes: the forecast is the idea's own product of scaled move and relative volatility, faded, and it is judged on the idea's 24-hour horizon.
Forecast: The forecast starts from VolatilityScaledReturnComponent with period 24, vol_period 168, vol_lookback 720 and lag 0. This is the 24-hour return in units of the 7-day hourly volatility, multiplied by that volatility over its 30-day (720-bar) mean, which is the usual-level convention. It is standardised against its own past values (window 500, min_periods 120) and then negated. The forecast is negative (short) after a rise and positive (long) after a fall. Its size grows with the size of the move in usual moves and with how far current volatility sits above its usual level. It is near zero when the move is small or volatility is unusually low. It is capped at ±20 and runs ungated on every bar.
Config: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use bars at positions 0, 24, 48, ... of each window, for each coin. On each such bar, compute forecast[t] / 10 × (close[t+24] / close[t] − 1 − the coin's mean 24-bar return over all windows). Then take the ordinary t of the pooled mean of that product.
- Supporting check: Among grid bars in the top fifth of |forecast| (per coin), compute sign(forecast) × excess 24-bar return. Its mean must exceed the same mean in the bottom fifth (Welch t ≥ 2). This shows the gain grows with position size.
- Confirm: The main measure's pooled mean is positive with t ≥ 2 over at least 1,000 independent cases, and the supporting check passes.
- Reject: The main measure's pooled mean is negative with t ≤ −2 over at least 1,000 independent cases.
- Inconclusive: Any of these results is inconclusive: - the main measure has |t| < 2; - the main measure has t ≥ 2 but the supporting check fails; - fewer than 1,000 non-overlapping cases are available.
