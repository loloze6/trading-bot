---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: nearness to the 90-day high had high predictive power for 5-day returns over the past 365 days -> kept: `ExcessPredictivePowerZComponent` w(t), a 365-day correlation of nearness (90-day high) with 5-day returns.
- Comparison: higher power means lower power over the following 90 days, a reversal from its usual level -> adapted: graded as w minus its 365-day mean, times the nearness z-score, negated so the reversal reads positive.
- Outcome: the stronger the upward reversal, the higher the 5-day return (longs only) -> kept: 5-bar forward return, long-only position grows with the reversal reading.
- Verdict transfer: yes: the forecast is the idea's reversal reading at its own windows, and the test reads the 5-day return that follows it.
Forecast: The forecast uses one component, `ExcessPredictivePowerZComponent`, with high_period 90, corr_lookback 365, horizon 5, z_window 365 and mean_window 365. Its value is (w − its 365-day mean) x z, where w is the past-365-day correlation of nearness to the 90-day high with 5-day returns, and z is the current nearness z-score. The value is standardised over its last 500 values, then negated, so it is positive when the relation's power is expected to turn the coin's nearness toward higher returns. It is then clipped at 0, so the forecast is long only. The forecast is zero when the reversal points down. It grows continuously with the strength of the upward reversal, up to the cap of 20.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, for cells with forecast > 0, take the coin's 5-bar return minus its normal 5-bar drift (all windows). Compute its forecast-weighted mean and the t of that mean over the cells.
- Supporting check: The book's mean daily timing gain is above 0. This is its mean daily return minus the gain from the market's own rise.
- Confirm: The forecast-weighted mean excess 5-bar return is above 0 with t >= 2, and the supporting check passes.
- Reject: The forecast-weighted mean excess 5-bar return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is a confirming t whose supporting check fails. A count below 100 grid cells with forecast > 0, over all coins and windows, is inconclusive whatever the t.
