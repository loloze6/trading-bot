---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: edf20a924da4
---
Fidelity:
- Situation: a large excess of the coin's past 365-day power of 90-day-high nearness for 5-day returns, times nearness's deviation from its usual level, pointing against a relation that implies a fall, after a 20-day rise -> adapted: the excess-power reading is negated and kept long-only, and "refuse after a 20-day fall" becomes a regime that is on while the 20-day return is positive.
- Comparison: power against its usual level, nearness against its usual level -> kept: `ExcessPredictivePowerZComponent` uses wbar over 365 days and the 365-day z of nearness.
- Outcome: the coin rises over the next 5 days, more so the higher its 20-day return -> kept: the 5-day excess return, with the grading by 20-day return tested in the supporting check.
- Verdict transfer: yes: the forecast is the reading the idea names, gated as it says, and the check tests its 20-day grading.
Forecast: The forecast uses `ExcessPredictivePowerZComponent` with `signal` "high", `high_period` 90, `corr_lookback` 365, `horizon` 5, `z_window` 365 and `mean_window` 365. Its value, (w − wbar) × z, is standardised over its past 365 values and negated, so the counter-bet against the implied fall reads positive. It is then clipped at 0, so the forecast is long only. Its size grows with the product of the excess power and the deviation of nearness. The forecast is active only while the 20-day return (`PriceEvolutionOnPeriodComponent`, 20) is above 0. After a 20-day fall the regime is flat. Elsewhere the forecast is 0 when the reading does not point against a fall.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, on grid bars with forecast > 0. Measure forecast × (the coin's 5-bar return minus its mean 5-bar return over all windows). Take the ordinary t of its mean, pooled over coins and windows, before costs.
- Supporting check: On those cases, the mean excess 5-bar return when the 20-day return (recomputed from closes) is above its median minus the mean excess return when it is below must be > 0.
- Confirm: The main measure's t is ≥ 2 and the supporting check's difference is > 0.
- Reject: The main measure's t is ≤ −2.
- Inconclusive: A t between −2 and 2 is inconclusive. So is a t ≥ 2 when the check fails. Fewer than 100 grid cases with forecast > 0 are also inconclusive.
