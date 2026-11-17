---
brief: 010_rsi-midline-regime-direction
source-idea: 010-08_rsi-below-streak-reversal
line: 7.b inconclusive
backtest: 010-08_rsi-below-streak-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days.
Consequence: The longer sellers have crowded in, the more positioning is exhausted, so the move reverses upward.
Why:
- F1: The tested effect points the way the idea predicts but is too small for 185 cases: the slope of the 14-day excess return on the forecast is +0.00186 (t 1.08); it is positive in both coins that ran (BTC t 0.82, n 89; ETH t 0.72, n 96); and the forecast thirds rise in order (-0.025, -0.005, +0.010 mean excess).
- F2: The data is too noisy for a gap that size: the 14-day excess returns have a standard deviation of about 0.14–0.19 in every run-length bin, while the bin means differ by only about 0.05; and only BTC and ETH ran (BNB is missing), giving 185 grid bars.
