---
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a large one-day move in a coin whose 20-day volatility is high -> adapted: the move's size is graded, and "volatility high" is a regime on the 20-day volatility rank.
- Comparison: the move and the 20-day volatility against the coin's usual level -> adapted: the day's return is divided by its own 60-day mean absolute return, so it grows with both the move and the current volatility.
- Outcome: part of the move is given back over the next 1 to 3 days -> adapted: the 1-to-3-day hold is dropped; the fade is re-set each bar, and the outcome is judged on 3-bar forward returns.
- Verdict transfer: yes: a fade sized by move times volatility, held only in high-volatility stretches, is what the idea predicts earns, and it must lose or earn nothing if the idea is false.
Forecast: The forecast is active only on bars where the 20-day volatility ranks in the upper half of its last 100 bars (VolatilityPercentileRegimeComponent, vol_period 20, lookback 100, smoothing 5, at 0.5 or above). On all other bars it is flat. On active bars it is minus the day's percent return (PriceEvolutionComponent, period 1), divided by the mean absolute daily return of the 60 bars before it and scaled to about 10. This measure is roughly (the move in 20-day usual moves) times (the 20-day volatility over its usual level). It then goes through signed_power with exponent 2, so small moves give almost no position and large ones give a large position. It is short after an up day and long after a down day, and 0 on a flat day.
Config: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are mean_reversion bars with a non-zero forecast, taken on a non-overlapping 3-bar grid in each window. For each case, take the coin's forward 3-bar return minus that coin's mean 3-bar return over all windows. Regress this excess return on the forecast and take the t of the slope.
- Supporting check: Over the 20% of cases with the largest |forecast|, the mean of sign(forecast) × excess 3-bar return is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check is above 0.
- Reject: The slope's t is -2 or less, meaning a larger fade forecast is followed by a continuation, not a give-back.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with the check failing. At least 100 independent cases are needed across coins and windows, and at least 20 in the top-20% group; with fewer, the result is inconclusive.
