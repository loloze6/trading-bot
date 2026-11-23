---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: edf20a924da4
---
Fidelity:
- Situation: the excess of the nearness signal's past 365-day power for 5-day returns over its usual level, times today's deviation of nearness to the 90-day high from its usual level, only while the 20-day return is negative and the 5-day return is positive -> kept: `ExcessPredictivePowerZComponent` ("high", 90, 365, 5) computes the joint reading, and a regime holds the two return conditions.
- Comparison: the reading points against a past relation that implies a rise -> kept: a positive reading implies a rise, so `negate` takes the counter-bet, sized by the reading's size.
- Outcome: the coin falls over the next 5 days, more as the joint reading grows -> kept: shorts only, each held 5 bars.
- Verdict transfer: yes: the config measures the idea's tradeable claim as stated, with its gate, side and horizon.
Forecast: The regime detector computes the 20-day and 5-day percent returns. On bars where the 20-day return is below 0 and the 5-day return is above 0, the regime is mean_reversion; on all other bars the forecast is 0 (flat). In mean_reversion, the forecast comes from `ExcessPredictivePowerZComponent`, which uses these settings: - signal: nearness to the 90-day closing high; - power: correlation with 5-day forward returns over the past 365 days, minus its mean over the prior 365 bars; - deviation: z-score of nearness over 365 bars. The reading is that excess power times today's deviation, standardised over its past 365 values (target 10, cap 20). It is then negated and clipped at max 0. The forecast is negative (short) when the reading is positive, that is, when the past relation implies a rise. It is 0 when the reading is negative or zero. The short grows linearly with the size of the reading.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, take the bars with forecast below 0. For each, compute (forecast / 10) x (close[t+5] / close[t] − 1 minus the coin's mean 5-bar return over all its windows). Report the t of the mean of these products, pooled over coins and windows.
- Supporting check: none
- Confirm: The mean product is positive with t ≥ 2, over at least 30 grid cases. This means larger shorts are followed by larger falls than the coin's normal drift.
- Reject: The mean product is negative with t ≤ −2, over at least 30 grid cases.
- Inconclusive: Any t between −2 and 2 is inconclusive. Fewer than 30 grid cases with a nonzero forecast is also inconclusive, whatever the t.
