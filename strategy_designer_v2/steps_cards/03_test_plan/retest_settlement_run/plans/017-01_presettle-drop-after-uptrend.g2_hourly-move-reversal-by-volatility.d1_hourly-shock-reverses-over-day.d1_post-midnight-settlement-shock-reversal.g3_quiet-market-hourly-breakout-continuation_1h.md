---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: 24-hour volatility low relative to 30-day volatility -> kept: a regime rule selects bars where the std of the last 24 hourly returns is below the std of the last 720.
- Comparison: 1-hour return relative to 24-hour volatility, the larger the stronger -> kept: the 1-bar return divided by the 24-bar return std, graded and signed.
- Outcome: next 24-hour return continues in the move's direction -> kept: long after an up hour, short after a down hour, each bet held 24 bars.
- Verdict transfer: yes: the test measures the stated condition, the stated graded size and the stated 24-hour continuation.
Forecast: Only on bars where the 24-hour volatility is below the 30-day volatility, the forecast is the current hour's return in units of the 24-hour return std. This is VolatilityScaledReturnComponent with period 1 and vol_period 24. It is standardised over the 60 previous values so that an average move gives about 10, capped at ±20. It is positive after an up hour and negative after a down hour, and its size grows linearly with the move's size in usual moves. On all other bars the regime is null and the forecast is 0.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use non-overlapping 24-bar grid cells of each window, keeping those whose start bar has a nonzero forecast. Regress the coin's next-24-bar return minus its normal 24-bar drift (all windows together) on the forecast at the cell's start bar, pooled over coins, and report the slope's t.
- Supporting check: The mean unusual move in the signal's direction, sign(forecast) × (24-bar return − drift), over the same cases is above 0.
- Confirm: Slope t ≥ 2 and the supporting check's mean is above 0, with at least 200 independent cases.
- Reject: Slope t ≤ −2 (moves of quiet hours reverse) with at least 200 independent cases.
- Inconclusive: A slope t between −2 and 2, or a t ≥ 2 with the check's mean not above 0, or fewer than 200 independent cases.
