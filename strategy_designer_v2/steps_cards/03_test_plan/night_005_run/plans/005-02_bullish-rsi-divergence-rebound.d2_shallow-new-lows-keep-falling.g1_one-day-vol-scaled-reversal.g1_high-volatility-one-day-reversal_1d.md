---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a vol-scaled 1-day move, weighted by how high 20-day volatility ranks against its past year -> kept: the move is the day's return over its 20-day volatility, and the weight is the 20-day volatility's rank over 365 bars, built by composing two components.
- Comparison: the higher the volatility rank, the stronger the reversal -> kept: the fade grows with the rank, roughly as the move times the rank.
- Outcome: the next 1 day moves against the day's move (up after falls, down after rises) -> kept: the horizon is 1 bar, contrarian on both sides.
- Verdict transfer: yes: the forecast is the idea's own interaction (fade times volatility rank), so its next-day payoff confirms or rejects the idea directly.
Forecast: The forecast combines two components, each standardised over 365 bars (min_periods 91). - B is VolatilityScaledReturnComponent (period 1, vol_period 20): the day's return in 20-day usual moves. It is negated. - A is RankWeightedScaledMoveComponent (abs_period 20, vol_period 20, lookback 365): the day's scaled move times (1 − the volatility's 365-bar rank). It has weight 0.5. - The rank averages about 0.5, so after standardising A ≈ 2·B·(1 − rank). - The forecast is (−B + 0.5A)/1.5 ≈ −B·rank/1.5. It is long after a fall and short after a rise, and its size grows with both the move and the volatility rank. - It is near zero when the move is small or volatility ranks low. It is graded and has no regime.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of a pooled regression of the next-bar coin return, less that coin's mean daily return over all windows, on the bar's forecast. It uses every bar of every window and coin, since 1-bar samples do not overlap.
- Supporting check: The book's timing gain (mean daily return minus its gain from the market's own rise) is above 0 before costs.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2, or t ≥ 2 with a failed supporting check. At least 1000 bars with a non-zero forecast are needed across coins and windows.
