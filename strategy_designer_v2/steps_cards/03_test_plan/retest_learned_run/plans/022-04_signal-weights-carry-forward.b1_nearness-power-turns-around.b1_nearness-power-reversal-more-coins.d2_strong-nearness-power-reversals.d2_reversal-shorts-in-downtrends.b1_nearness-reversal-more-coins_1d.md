---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the nearness to the 90-day high deviates from its usual level while that signal's past 365-day power for 5-day returns is above its usual level, and the reading implies a rise -> kept: ExcessPredictivePowerZComponent, negated and clipped to its short side.
- Comparison: past power against its usual level, and today's nearness against its usual level -> kept: w minus its 365-day mean, times the 365-day z-score of nearness.
- Outcome: the coin falls over the next 5 days, more as the joint reading grows, only while its 20-day return is negative -> kept: 5-bar horizon; the condition is a regime rule on the 20-day return being below 0.
- Verdict transfer: yes: the forecast is the idea's own joint reading, short only, active only in falling coins, judged on the fall that follows over 5 days.
Forecast: The main indicator is the excess-power reading for nearness to the 90-day closing high. It takes the 365-day correlation of nearness with the coin's 5-day forward return and subtracts that correlation's 365-day mean. It then multiplies the result by the 365-day z-score of today's nearness. The reading is positive when the past relation implies a rise. It is standardised over its last 500 values (min 120), negated, and clipped at 0, so the forecast is a short that grows with the joint reading. It is 0 when the reading implies no rise. The regime detector reads the 20-day return (PriceEvolutionComponent, period 20). On bars where that return is below 0 the short is active. On every other bar the book is flat. The forecast is never positive.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure uses cases: bars on each window's 5-bar grid where the forecast is below 0. For each case, take the coin's 5-bar return from that close minus the coin's mean 5-bar return over all its windows. Flip the sign so that a fall counts as positive, and weight it by abs(forecast) / mean abs(forecast) over the cases. The measure is the mean of these values, with its t of the mean.
- Supporting check: Among the cases, the least-squares slope of the drift-removed 5-bar return on abs(forecast) is below 0 (larger shorts, larger falls).
- Confirm: The weighted mean fall is above 0 with t >= 2, and the slope check passes.
- Reject: The weighted mean is below 0 with t <= -2, meaning the coins rose beyond their drift after the shorts.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 whose slope is not below 0 is also inconclusive. So is any result from fewer than 100 non-overlapping cases over all coins and windows.
