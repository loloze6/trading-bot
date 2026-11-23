---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's excess past power of 90-day-high nearness, times today's nearness deviation from its usual level -> kept: `ExcessPredictivePowerZComponent` computes (w − wbar) × z, with w over 365 days, the 5-day horizon and the 90-day high.
- Comparison: past 365-day power against its usual level, and nearness against its usual level -> kept: wbar is the mean of past w over 365 days, and z is computed over 365 days.
- Outcome: the coin moves against the past relation over the next 5 days, more as both factors grow -> kept: `negate` takes the counter-bet, and the size grows with the product.
- Verdict transfer: yes: the forecast is the idea's own joint reading, traded against the past relation over its 5-day horizon.
Forecast: The forecast is computed every day from the nearness signal, which is the close over its highest close of the last 90 days, minus 1. - Raw value. Its power is its correlation with 5-day forward returns over the past 365 days. The component takes that power minus the mean of the power over the 365 days before. It multiplies this excess by today's z-score of nearness over 365 days. - Scaling. The product is standardised over its last 500 values (min_periods 120), then negated, so the bet runs against the past relation. - Dead zone. `signed_power` with exponent 2 (pivot 10) damps small readings towards 0 and amplifies large ones. Fees then go mainly to large joint readings. - Sign. The forecast is positive when the excess power and the nearness deviation have opposite signs. It is negative when they share a sign. It is near zero when either factor is near zero. Its size grows with the square of the joint reading.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-day return, minus its normal drift (its mean 5-day return over all windows), on the forecast. Each coin and window uses a non-overlapping 5-bar grid. The slope is pooled over coins and windows, with its t.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise (the timing part), is above 0.
- Confirm: The slope is positive with t ≥ 2, and the timing part of the book's mean daily return is above 0.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive. A slope with t ≥ 2 while the timing part is at or below 0 is also inconclusive. Fewer than 300 grid cases with a nonzero forecast is inconclusive.
