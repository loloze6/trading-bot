---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the reversal of the nearness-to-90-day-high signal's 365-day predictive power for 5-day returns, pointing up, in proportion to its strength -> kept: the negated `ExcessPredictivePowerZComponent` (high_period 90, corr_lookback 365, horizon 5), clipped at 0.
- Comparison: higher past-365-day power means lower power over the following 90 days, only while the 30-day return is positive -> kept: power is judged against its own past mean, and a regime on the 30-day return gates the bet.
- Outcome: the coin's return over the next 5 days is higher -> kept: the book holds each bet for 5 daily bars.
- Verdict transfer: yes: the forecast is the idea's reversal reading, in the idea's rising coins, judged on its own 5-day returns.
Forecast: The forecast starts from `ExcessPredictivePowerZComponent` with these settings: - high_period 90, corr_lookback 365, horizon 5, z_window 365, mean_window 365. - It computes (w − wbar) × z: - w is the 365-day correlation of nearness-to-90-day-high with the next 5-day return. - wbar is w's mean over the prior 365 days. - z is the z-score of today's nearness to the high. How the forecast is built and sized: - The value is negated, which gives the reversal bet. It is positive in two cases: - power is below its usual level and the close sits nearer its high than usual; - power is above its usual level and the close sits further from its high than usual. - It is standardised against its own past 365 values, then clipped at 0, so the forecast is long only. - It is active only on bars where the 30-day return is above 0 (regime `trending`). Every other bar is flat. - The forecast grows with the size of the reversal reading and is 0 when that reading points down.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, pooled over coins and windows, regress the coin's 5-bar return minus its normal 5-bar drift (holding the coin) on the forecast. The measure is the slope and its t.
- Supporting check: The book's timing gain before costs is above 0. This is its mean daily gain minus the part due to the coin's own rise.
- Confirm: The slope is above 0 with t ≥ 2, over at least 100 grid cases with a forecast above 0, and the timing gain is above 0.
- Reject: The slope is below 0 with t ≤ −2, over at least 100 grid cases with a forecast above 0.
- Inconclusive: Any of these is inconclusive: - a t between −2 and 2; - a confirming slope with a timing gain at or below 0; - fewer than 100 grid cases with a forecast above 0.
