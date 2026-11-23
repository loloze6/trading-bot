---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: excess past 365-day power of 90-day-high nearness for 5-day returns, times nearness's deviation from its usual level, while the 20-day return is negative -> kept (ExcessPredictivePowerZComponent 90/365/5/365/365, gated by a 20-day-return regime rule)
- Comparison: past power against its own usual level, and nearness against its usual level -> kept (w − wbar over 365 days; z over 365 days)
- Outcome: when the reading implies a rise, the coin falls over the next 5 days, larger for a larger reading -> kept (negated reading, short side only, 5-bar hold)
- Verdict transfer: yes: the forecast is the idea's joint reading, short only on falling coins, so a confirm or reject of its 5-day falls transfers to the idea.
Forecast: The forecast uses ExcessPredictivePowerZComponent with high_period 90, corr_lookback 365, horizon 5, z_window 365 and mean_window 365. Its value is (the nearness signal's past power minus its usual power) times the z-score of nearness. The value is standardised over 500 past values, then negated, then clipped at max 0. The forecast is negative (short) when the reading implies a rise, and its size grows with the product of the two deviations. It is zero when the reading implies a fall. The forecast is active only on bars where the coin's 20-day return is below 0, through a regime rule on PriceEvolutionOnPeriodComponent(20). On all other bars the regime is null and the coin is flat.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are bars on each window's non-overlapping 5-bar grid where forecast ≤ −2. For each case, take the coin's 5-bar return minus its mean 5-bar return over all windows (holding the coin). Sign it as a short gain and weight it by |forecast|/10. Report the t of the mean over cases, pooled across coins, before costs.
- Supporting check: The mean excess fall of cases with |forecast| above the median of |forecast| minus that of cases below the median is greater than 0.
- Confirm: The main-measure t is 2 or more, with at least 30 cases, and the supporting check is above 0.
- Reject: The main-measure t is −2 or less, with at least 30 cases: the weighted short cases rose more than the coin's drift.
- Inconclusive: A t between −2 and 2 is inconclusive. A t of 2 or more with a failed supporting check is inconclusive. Fewer than 30 cases is inconclusive.
